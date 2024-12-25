from datetime import UTC, datetime, timedelta
from typing import Any

import httpx
from httpx._types import RequestContent, RequestFiles
from loguru._logger import Logger
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from skys_llc_auth.databases import DatabaseConfig
from skys_llc_auth.exceptions import RequestError
from skys_llc_auth.models import CredentialStorage
from skys_llc_auth.schemas import Credentails


class RequestBetweenMicroservices:
    def __init__(
        self,
        refresh_url: str,
        login_url: str,
        name: str,
        access: str,
        refresh: str,
        login: str,
        password: str,
        retries: int,
        db_config: DatabaseConfig,
        logger: Logger,
        token_lifetime: int = 1440,
    ):
        self.refresh_url = refresh_url
        self.login_url = login_url
        self.name = name
        self.access_token = access
        self.refresh_token = refresh
        self.login = login
        self.password = password
        self.transport = httpx.AsyncHTTPTransport(retries=retries)
        self.headers = {}
        self.db_config = db_config
        self.token_lifetime = token_lifetime
        self.logger = logger
        self.session = None

    async def _send_request(
        self,
        method: str,
        url: str,
        content: RequestContent | None = None,
        data: dict[str, Any] | None = None,
        files: RequestFiles | None = None,
        json: Any | None = None,
        headers: dict[str, str] | None = None,
        params: dict[str, Any] | None = None,
        timeout: float | None = None,
    ) -> httpx.Response:
        """Function for send async request to another microservices"""
        self.logger.info(f"Request with microservices token to {url} with {method} method")

        async with httpx.AsyncClient(transport=self.transport) as client:
            response = await client.request(
                method,
                url,
                content=content,
                data=data,
                files=files,
                json=json,
                params=params,
                headers=headers,
                timeout=timeout,
            )
            self.logger.info(f"Response ending with status code:{response.status_code} body:{response.text}")

        return response

    async def request_with_microservice_tokens(
        self,
        method: str,
        url: str,
        *args: Any,
        **kwargs: Any,
    ) -> httpx.Response:
        self.logger.info(f"Enter in function to send request with microservices token to {url} with {method} method")
        """Function for send async request to another microservices and validate credentials"""
        if not self.access_token:
            self.logger.info("Access token is not present")
            await self.logging_in()

        auth = {"Authorization": "Bearer " + self.access_token}
        self.headers = kwargs.get("headers", {})
        self.headers.update(auth)
        self.logger.info("Trying first request")
        response = await self._send_request(method=method, url=url, headers=self.headers, *args, **kwargs)  # noqa: B026
        self.logger.info(f"Request end with status code: {response.status_code} body: {response.text}")
        if response.status_code == 401:
            self.logger.info("First request end with status code: 401")

            refreshed_token_pair = await self.refresh_tokens()

            if refreshed_token_pair.status_code == 401:
                self.logger.info("Refresh token request end with status code: 401")

                await self.logging_in()

                self.headers.update({"Authorization": "Bearer " + self.access_token})

                return await self._send_request(method=method, url=url, headers=self.headers, *args, **kwargs)  # noqa: B026

            return await self._send_request(method=method, url=url, headers=self.headers, *args, **kwargs)  # noqa: B026

        return response

    async def logging_in(self) -> httpx.Response:
        """Function for send async request to users and get tokens"""
        cred = await self.get_credentials_from_table()
        if cred:
            self.access_token = cred.access_token
            self.refresh_token = cred.refresh_token
            self.login = cred.login
            self.password = cred.password
            self.logger.info(f"Cred {self.name} found in db")

        response = await self._send_request(
            "POST", self.login_url, json={"login": self.login, "password": self.password}
        )

        if response.status_code == 401:
            self.logger.error("An error while logging, try to get cred form db")
            cred = await self.get_credentials_from_table()
            if not cred:
                self.logger.error("An error while getting cred form db")
                raise RequestError(f"Cred {self.name} dissapeared")

            second_try = await self._send_request(
                "POST", self.login_url, json={"login": cred.login, "password": cred.password}
            )
            if second_try.status_code == 401:
                self.logger.error("An error while getting cred form db")
                raise RequestError(f"Login failed for {self.name} because refresh_token: {self.refresh_token}")

            if second_try.status_code == 201:
                self.access_token = second_try.json().get("access_token", "")
                self.refresh_token = second_try.json().get("refresh_token", "")
                await self.validate_entity()

        elif response.status_code == 201:
            self.logger.info("Logging successfully completed")
            self.access_token = response.json().get("access_token", "")
            self.refresh_token = response.json().get("refresh_token", "")
            await self.validate_entity()

        else:
            self.logger.error("An error while logging")
            raise RequestError(
                f"Login failed for {self.name} because login: {self.login} password: {self.password} response: {response.text}"
            )

        return response

    async def refresh_tokens(self) -> httpx.Response:
        """Function for send async request to users and refresh new tokens"""
        response = await self._send_request(
            "POST",
            self.refresh_url,
            headers={"Authorization": "Bearer " + self.refresh_token},
        )
        if response.status_code == 401:
            raise RequestError(f"Login failed for {self.name} because refresh_token: {self.refresh_token}")

        if response.status_code == 201:
            self.access_token = response.json().get("access_token", "")
            self.refresh_token = response.json().get("refresh_token", "")

        return response

    async def insert_credentials_to_table(
        self,
        payload: Credentails,
        db: AsyncSession,
    ) -> CredentialStorage | None:
        stmt = CredentialStorage(**payload.model_dump())
        db.add(stmt)
        await db.commit()
        return stmt

    async def get_credentials_from_table(
        self,
        db: AsyncSession | None = None,
    ) -> CredentialStorage | None:
        query = (
            select(CredentialStorage)
            .where(CredentialStorage.service_name == self.name)
            .order_by(CredentialStorage.created_at.desc())
            .limit(1)
        )
        if db is None:
            db = await self._get_async_session()
            result = await db.execute(query)

            return result.scalar()

        result = await db.execute(query)
        return result.scalar()

    async def update_credentials_to_table(
        self,
        payload: Credentails,
        db: AsyncSession,
    ):
        query = (
            update(CredentialStorage)
            .where(CredentialStorage.service_name == self.name)
            .values(**payload.model_dump(exclude_none=True))
            .returning(CredentialStorage)
        )
        result = await db.execute(query)
        await db.commit()
        return result.scalar()

    async def _get_async_session(self) -> AsyncSession:
        it = self.db_config.get_async_session()
        self.session = await it.__anext__()
        return self.session

    async def validate_entity(self):
        payload = Credentails(
            access_token=self.access_token,
            refresh_token=self.refresh_token,
            login=self.login,
            password=self.password,
            service_name=self.name,
            access_until=datetime.now(UTC) + timedelta(seconds=self.token_lifetime),
            created_at=datetime.now(UTC),
        )
        async with self.db_config.async_session_maker() as db:
            if await self.get_credentials_from_table(db=db):
                self.logger.info(f"Credentials for {self.name} already exist")
                await self.update_credentials_to_table(payload=payload, db=db)
                self.logger.info(f"Credentials for {self.name} updated")

            else:
                await self.insert_credentials_to_table(payload=payload, db=db)
                self.logger.info(f"Credentials for {self.name} inserting")
