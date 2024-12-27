import json
from typing import Annotated

import bcrypt
from fastapi import APIRouter, status, HTTPException, Header
from fastapi.responses import JSONResponse
from requests import HTTPError
from square_commons import get_api_output_in_standard_format

from square_administration.configuration import (
    global_object_square_logger,
    config_str_admin_password_hash,
    global_object_square_authentication_helper,
    global_int_app_id,
)
from square_administration.messages import messages
from square_administration.pydantic_models.authentication import (
    RegisterUsernameV0,
    LoginUsernameV0,
)

router = APIRouter(
    tags=["authentication"],
)


@router.post("/register_username/v0")
@global_object_square_logger.async_auto_logger
async def register_username_v0(
    body: RegisterUsernameV0,
):
    username = body.username
    password = body.password
    admin_password = body.admin_password

    username = username.lower()
    try:
        """
        validation
        """

        # validation for admin_password
        if not (
            bcrypt.checkpw(
                admin_password.encode("utf-8"),
                config_str_admin_password_hash.encode("utf-8"),
            )
        ):
            output_content = get_api_output_in_standard_format(
                message=messages["INCORRECT_PASSWORD"],
                log=f"incorrect admin password.",
            )
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=output_content,
            )

        """
        main process
        """
        response = global_object_square_authentication_helper.register_username_v0(
            username=username,
            password=password,
            app_id=global_int_app_id,
        )
        """
        return value
        """
        output_content = get_api_output_in_standard_format(
            message=messages["REGISTRATION_SUCCESSFUL"],
            data={"main": response["data"]["main"]},
        )
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=output_content,
        )
    except HTTPError as http_error:
        global_object_square_logger.logger.error(http_error, exc_info=True)
        """
        rollback logic
        """
        # pass
        return JSONResponse(
            status_code=http_error.response.status_code,
            content=json.loads(http_error.response.content),
        )
    except HTTPException as http_exception:
        global_object_square_logger.logger.error(http_exception, exc_info=True)
        """
        rollback logic
        """
        # pass
        return JSONResponse(
            status_code=http_exception.status_code, content=http_exception.detail
        )
    except Exception as e:
        global_object_square_logger.logger.error(e, exc_info=True)
        """
        rollback logic
        """
        # pass
        output_content = get_api_output_in_standard_format(
            message=messages["GENERIC_500"],
            log=str(e),
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=output_content
        )


@router.post("/login_username/v0")
@global_object_square_logger.async_auto_logger
async def login_username_v0(
    body: LoginUsernameV0,
):
    username = body.username
    password = body.password

    try:
        """
        validation
        """
        # pass
        """
        main process
        """
        response = global_object_square_authentication_helper.login_username_v0(
            username=username,
            password=password,
            app_id=global_int_app_id,
            assign_app_id_if_missing=False,
        )
        """
        return value
        """
        output_content = get_api_output_in_standard_format(
            message=messages["LOGIN_SUCCESSFUL"],
            data={"main": response["data"]["main"]},
        )
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=output_content,
        )
    except HTTPError as http_error:
        global_object_square_logger.logger.error(http_error, exc_info=True)
        """
        rollback logic
        """
        # pass
        return JSONResponse(
            status_code=http_error.response.status_code,
            content=json.loads(http_error.response.content),
        )
    except HTTPException as http_exception:
        global_object_square_logger.logger.error(http_exception, exc_info=True)
        """
        rollback logic
        """
        # pass
        return JSONResponse(
            status_code=http_exception.status_code, content=http_exception.detail
        )
    except Exception as e:
        global_object_square_logger.logger.error(e, exc_info=True)
        """
        rollback logic
        """
        # pass
        output_content = get_api_output_in_standard_format(
            message=messages["GENERIC_500"],
            log=str(e),
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=output_content
        )


@router.patch("/remove_app_for_self/v0")
@global_object_square_logger.async_auto_logger
async def remove_app_for_self_v0(
    access_token: Annotated[str, Header()],
):

    try:
        """
        validation
        """
        # pass
        """
        main process
        """
        response = global_object_square_authentication_helper.update_user_app_ids_v0(
            access_token=access_token,
            app_ids_to_add=[],
            app_ids_to_remove=[global_int_app_id],
        )
        """
        return value
        """
        output_content = get_api_output_in_standard_format(
            message=messages["GENERIC_UPDATE_SUCCESSFUL"],
            data={"main": response["data"]["main"]},
        )
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=output_content,
        )
    except HTTPError as http_error:
        global_object_square_logger.logger.error(http_error, exc_info=True)
        """
        rollback logic
        """
        # pass
        return JSONResponse(
            status_code=http_error.response.status_code,
            content=json.loads(http_error.response.content),
        )
    except HTTPException as http_exception:
        global_object_square_logger.logger.error(http_exception, exc_info=True)
        """
        rollback logic
        """
        # pass
        return JSONResponse(
            status_code=http_exception.status_code, content=http_exception.detail
        )
    except Exception as e:
        global_object_square_logger.logger.error(e, exc_info=True)
        """
        rollback logic
        """
        # pass
        output_content = get_api_output_in_standard_format(
            message=messages["GENERIC_500"],
            log=str(e),
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=output_content
        )
