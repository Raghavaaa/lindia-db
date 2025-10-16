"""Repository layer for clean data access."""

from repositories.user_repo import (
    create_user,
    get_user_by_id,
    get_by_email,
    list_users,
    update_user,
    delete_user
)

from repositories.client_repo import (
    create_client,
    get_client_by_id,
    list_clients_for_lawyer,
    update_client,
    delete_client
)

from repositories.case_repo import (
    create_case,
    get_case_by_id,
    list_cases_for_client,
    update_case,
    delete_case
)

from repositories.property_opinion_repo import (
    create_property_opinion,
    get_property_opinion_by_id,
    list_property_opinions_by_client,
    update_property_opinion,
    delete_property_opinion
)

from repositories.research_repo import (
    create_research_query,
    get_research_query_by_id,
    list_research_by_lawyer,
    search_queries,
    update_research_query,
    delete_research_query
)

from repositories.junior_repo import (
    append_log,
    get_junior_log_by_id,
    list_junior_logs_by_lawyer
)

from repositories.inference_repo import (
    log_inference,
    get_inference_log_by_id,
    list_inference_logs_by_query
)

from repositories.upload_repo import (
    create_upload,
    get_upload_by_id,
    list_uploads_by_user,
    list_uploads_by_client,
    list_uploads_by_tab,
    update_upload,
    delete_upload
)

__all__ = [
    # User
    "create_user", "get_user_by_id", "get_by_email", "list_users",
    "update_user", "delete_user",
    # Client
    "create_client", "get_client_by_id", "list_clients_for_lawyer",
    "update_client", "delete_client",
    # Case
    "create_case", "get_case_by_id", "list_cases_for_client",
    "update_case", "delete_case",
    # Property Opinion
    "create_property_opinion", "get_property_opinion_by_id",
    "list_property_opinions_by_client", "update_property_opinion",
    "delete_property_opinion",
    # Research
    "create_research_query", "get_research_query_by_id",
    "list_research_by_lawyer", "search_queries",
    "update_research_query", "delete_research_query",
    # Junior
    "append_log", "get_junior_log_by_id", "list_junior_logs_by_lawyer",
    # Inference
    "log_inference", "get_inference_log_by_id", "list_inference_logs_by_query",
    # Upload
    "create_upload", "get_upload_by_id", "list_uploads_by_user",
    "list_uploads_by_client", "list_uploads_by_tab", "update_upload", "delete_upload"
]

