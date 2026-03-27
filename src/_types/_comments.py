from __future__ import annotations

from typing_extensions import Any, TypedDict


class Children(TypedDict):
    kind: str
    data: Data


class ResponseComment(TypedDict):
    after: str
    dist: int
    modhash: str
    geo_filter: str
    children: list[Children]
    before: None
    subreddit_id: str
    approved_at_utc: None
    author_is_blocked: bool
    comment_type: None
    link_title: str
    mod_reason_by: None
    banned_by: None
    ups: int
    num_reports: None
    author_flair_type: str
    total_awards_received: int
    subreddit: str
    link_author: str
    likes: None
    replies: str
    user_reports: list[Any]
    saved: bool
    id: str
    banned_at_utc: None
    mod_reason_title: None
    gilded: int
    archived: bool
    collapsed_reason_code: None
    no_follow: bool
    author: str
    num_comments: int
    can_mod_post: bool
    send_replies: bool
    parent_id: str
    score: int
    author_fullname: str
    over_18: bool
    report_reasons: None
    removal_reason: None
    approved_by: None
    controversiality: int
    body: str
    edited: bool
    top_awarded_type: None
    downs: int
    author_flair_css_class: None
    is_submitter: bool
    collapsed: bool
    author_flair_richtext: list[Any]
    author_patreon_flair: bool
    body_html: str
    gildings: Any
    collapsed_reason: None
    distinguished: None
    associated_award: None
    stickied: bool
    author_premium: bool
    can_gild: bool
    link_id: str
    unrepliable_reason: None
    author_flair_text_color: None
    score_hidden: bool
    permalink: str
    subreddit_type: str
    link_permalink: str
    name: str
    author_flair_template_id: None
    subreddit_name_prefixed: str
    author_flair_text: None
    treatment_tags: list[Any]
    created: float
    created_utc: float
    awarders: list[Any]
    all_awardings: list[Any]
    locked: bool
    author_flair_background_color: None
    collapsed_because_crowd_control: None
    mod_reports: list[Any]
    quarantine: bool
    mod_note: None
    link_url: str


class Data(TypedDict):
    after: str
    dist: int
    modhash: str
    children: list[ResponseComment]


class RedditCommentResponse(TypedDict):
    kind: str
    data: Data
