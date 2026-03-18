from typing import TypedDict, List, Optional, Any


class MediaEmbed(TypedDict):
    pass


class SecureMediaEmbed(TypedDict):
    pass


class Gildings(TypedDict):
    pass


class Thread(TypedDict):
    approved_at_utc: Optional[Any]
    subreddit: str
    selftext: str
    author_fullname: str
    saved: bool
    mod_reason_title: Optional[Any]
    gilded: int
    clicked: bool
    title: str
    link_flair_richtext: List[Any]
    subreddit_name_prefixed: str
    hidden: bool
    pwls: Optional[Any]
    link_flair_css_class: Optional[Any]
    downs: int
    top_awarded_type: Optional[Any]
    hide_score: bool
    name: str
    quarantine: bool
    link_flair_text_color: str
    upvote_ratio: int
    author_flair_background_color: Optional[Any]
    subreddit_type: str
    ups: int
    total_awards_received: int
    media_embed: MediaEmbed
    author_flair_template_id: Optional[Any]
    is_original_content: bool
    user_reports: List[Any]
    secure_media: Optional[Any]
    is_reddit_media_domain: bool
    is_meta: bool
    category: Optional[Any]
    secure_media_embed: SecureMediaEmbed
    link_flair_text: Optional[Any]
    can_mod_post: bool
    score: int
    approved_by: Optional[Any]
    is_created_from_ads_ui: bool
    author_premium: bool
    thumbnail: str
    edited: bool
    author_flair_css_class: Optional[Any]
    author_flair_richtext: List[Any]
    gildings: Gildings
    content_categories: Optional[Any]
    is_self: bool
    mod_note: Optional[Any]
    created: int
    link_flair_type: str
    wls: Optional[Any]
    removed_by_category: Optional[Any]
    banned_by: Optional[Any]
    author_flair_type: str
    domain: str
    allow_live_comments: bool
    selftext_html: str
    likes: Optional[Any]
    suggested_sort: Optional[Any]
    banned_at_utc: Optional[Any]
    url_overridden_by_dest: str
    view_count: Optional[Any]
    archived: bool
    no_follow: bool
    is_crosspostable: bool
    pinned: bool
    over_18: bool
    all_awardings: List[Any]
    awarders: List[Any]
    media_only: bool
    can_gild: bool
    spoiler: bool
    locked: bool
    author_flair_text: Optional[Any]
    treatment_tags: List[Any]
    visited: bool
    removed_by: Optional[Any]
    num_reports: Optional[Any]
    distinguished: Optional[Any]
    subreddit_id: str
    author_is_blocked: bool
    mod_reason_by: Optional[Any]
    removal_reason: Optional[Any]
    link_flair_background_color: str
    id: str
    is_robot_indexable: bool
    report_reasons: Optional[Any]
    author: str
    discussion_type: Optional[Any]
    num_comments: int
    send_replies: bool
    contest_mode: bool
    mod_reports: List[Any]
    author_patreon_flair: bool
    author_flair_text_color: Optional[Any]
    permalink: str
    stickied: bool
    url: str
    subreddit_subscribers: int
    created_utc: int
    num_crossposts: int
    media: Optional[Any]
    is_video: bool


class Children(TypedDict):
    kind: str
    data: Thread


class Data(TypedDict):
    after: str
    dist: int
    modhash: str
    geo_filter: str
    children: List[Children]


class RedditResponse(TypedDict):
    kind: str
    data: Data
