from gh_hooks_utils.payloads import (
    DiscussionCommentEvent,
    DiscussionEvent,
    GithubWebhookEvent,
    InstallationEvent,
    InstallationRepositoriesEvent,
    PullRequestEvent,
)


def test_events_are_github_webhook_event():
    assert issubclass(DiscussionCommentEvent, GithubWebhookEvent)
    assert issubclass(DiscussionEvent, GithubWebhookEvent)
    assert issubclass(InstallationEvent, GithubWebhookEvent)
    assert issubclass(InstallationRepositoriesEvent, GithubWebhookEvent)
    assert issubclass(PullRequestEvent, GithubWebhookEvent)
