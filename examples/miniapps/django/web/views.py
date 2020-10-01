"""Views module."""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from dependency_injector.wiring import Provide

from githubnavigator.containers import Container
from githubnavigator.services import SearchService


def index(
        request: HttpRequest,
        search_service: SearchService = Provide[Container.search_service],
        default_query: str = Provide[Container.config.default.query],
        default_limit: int = Provide[Container.config.default.limit.as_int()],
) -> HttpResponse:
    query = request.GET.get('query', default_query)
    limit = int(request.GET.get('limit', default_limit))

    repositories = search_service.search_repositories(query, limit)

    return render(
        request,
        template_name='index.html',
        context={
            'query': query,
            'limit': limit,
            'limits': [5, 10, 20],
            'repositories': repositories,
        }
    )
