from __future__ import annotations

from collections.abc import Collection
from dataclasses import is_dataclass
from functools import partial
from types import NoneType
from typing import TYPE_CHECKING
from unittest import TestCase
from unittest.mock import MagicMock
from uuid import uuid4

from jsonrpc import BatchRequest, Error, ErrorEnum, Request

if TYPE_CHECKING:
    from typing import Any
    from uuid import UUID


class TestRequest(TestCase):
    @property
    def random_id(self) -> int:
        uuid: UUID = uuid4()
        return int(uuid)

    def test_inheritance(self) -> None:
        request: Request = Request(method="request0", request_id=self.random_id)
        self.assertTrue(is_dataclass(request))

    def test_validate_method(self) -> None:
        for invalid_request in (
            partial(Request, method=None),
            partial(Request, method="rpc.request1"),
        ):
            with self.subTest(request=invalid_request):
                with self.assertRaises(Error) as context:
                    invalid_request(request_id=self.random_id)

                self.assertEqual(context.exception.code, ErrorEnum.INVALID_REQUEST)
                self.assertEqual(
                    context.exception.message,
                    "Request method must be a string and should not have a 'rpc.' prefix",
                )

        request: Request = Request(method="request2")
        self.assertEqual(request.method, "request2")

    def test_validate_params(self) -> None:
        with self.assertRaises(Error) as context:
            Request(method="request3", params=None)

        self.assertEqual(context.exception.code, ErrorEnum.INVALID_REQUEST)
        self.assertEqual(
            context.exception.message,
            f"Request params must be a sequence or mapping, not a {NoneType.__name__!r}",
        )

        for request, (expected_args, expected_kwargs) in (
            (
                Request(method="request4", params=["1024", "2048", "4096"]),
                (("1024", "2048", "4096"), {}),
            ),
            (
                Request(method="request5", params={"a": 1024, "b": 2048}),
                ((), {"a": 1024, "b": 2048}),
            ),
        ):
            with self.subTest(request=request, expected_args=expected_args, expected_kwargs=expected_kwargs):
                self.assertTupleEqual(request.args, expected_args)
                self.assertDictEqual(request.kwargs, expected_kwargs)

    def test_validate_request_id(self) -> None:
        with self.assertRaises(Error) as context:
            Request(method="request6", request_id=None)

        self.assertEqual(context.exception.code, ErrorEnum.INVALID_REQUEST)
        self.assertEqual(
            context.exception.message,
            f"Request id must be an optional string or number, not a {NoneType.__name__!r}",
        )

        request: Request = Request(method="request7", request_id=(request_id := self.random_id))
        self.assertEqual(request.request_id, request_id)

    def test_is_notification(self) -> None:
        request: Request = Request(method="request12", request_id=self.random_id)
        self.assertFalse(request.is_notification)

        notification: Request = Request(method="request13")
        self.assertTrue(notification.is_notification)

    def test_from_json(self) -> None:
        errors: tuple[Error, ...] = (
            Request.from_json(None),
            Request.from_json({}),
            Request.from_json({"jsonrpc": "2.0"}),
            Request.from_json({"jsonrpc": "2.1", "method": "request14"}),
            Request.from_json({"jsonrpc": "2.0", "method": None}),
            Request.from_json({"jsonrpc": "2.0", "method": "request15", "params": None}),
            Request.from_json({"jsonrpc": "2.0", "method": "request16", "id": None}),
        )
        for error in errors:
            with self.subTest(error=error):
                self.assertIsInstance(error, Error)

        requests: tuple[Request, ...] = (
            Request.from_json({"jsonrpc": "2.0", "method": "request17", "params": ["1024", "2048", "4096"], "id": self.random_id}),
            Request.from_json({"jsonrpc": "2.0", "method": "request18", "params": {"a": 1024, "b": 2048}}),
            Request.from_json({"jsonrpc": "2.0", "method": "request19", "id": self.random_id}),
            Request.from_json({"jsonrpc": "2.0", "method": "request20"}),
        )
        for request in requests:
            with self.subTest(request=request):
                self.assertIsInstance(request, Request)


class TestBatchRequest(TestCase):
    @property
    def random_id(self) -> str:
        uuid: UUID = uuid4()
        return str(uuid)

    def test_inheritance(self) -> None:
        mock: MagicMock = MagicMock()
        batch_request: BatchRequest = BatchRequest([mock])

        self.assertTrue(is_dataclass(batch_request))
        self.assertIsInstance(batch_request, Collection)
        self.assertIn(mock, batch_request)
        self.assertEqual(len(batch_request), 1)

        for request in batch_request:
            with self.subTest(request=request):
                self.assertIs(request, mock)

    def test_from_json(self) -> None:
        invalid_requests: list[dict[str, Any] | None] = [
            None,
            {},
            {"jsonrpc": "2.0"},
            {"jsonrpc": "2.1", "method": "request6"},
            {"jsonrpc": "2.0", "method": None},
            {"jsonrpc": "2.0", "method": "request7", "params": None},
            {"jsonrpc": "2.0", "method": "request8", "id": None},
        ]
        invalid_batch_request: BatchRequest = BatchRequest.from_json(invalid_requests)
        self.assertEqual(len(invalid_requests), len(invalid_batch_request))

        for request in invalid_batch_request:
            with self.subTest(request=request):
                self.assertIsInstance(request, Error)

        requests: list[dict[str, Any]] = [
            {"jsonrpc": "2.0", "method": "request9", "params": ["1024", "2048", "4096"], "id": self.random_id},
            {"jsonrpc": "2.0", "method": "request10", "params": {"a": 1024, "b": 2048}},
            {"jsonrpc": "2.0", "method": "request11", "id": self.random_id},
            {"jsonrpc": "2.0", "method": "request12"},
        ]
        batch_request: BatchRequest = BatchRequest.from_json(requests)
        self.assertEqual(len(requests), len(batch_request))

        for request in batch_request:
            with self.subTest(request=request):
                self.assertIsInstance(request, Request)
