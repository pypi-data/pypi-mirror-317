push_card = [
    {
        "type": "card",
        "theme": "secondary",
        "size": "lg",
        "modules": [
            {
                "type": "header",
                "text": {"type": "plain-text", "content": "🚀 @{commiter} 推送了代码"},
            },
            {
                "type": "section",
                "text": {
                    "type": "paragraph",
                    "cols": 3,
                    "fields": [
                        {"type": "kmarkdown", "content": "**📦 仓库**\n{repository}"},
                        {"type": "kmarkdown", "content": "**🔀 分支**\n{branch}"},
                        {"type": "kmarkdown", "content": "**🕒 日期**\n{time}"},
                    ],
                },
            },
            {
                "type": "section",
                "text": {"type": "kmarkdown", "content": "**📝 提交信息**\n{message}"},
                "mode": "right",
                "accessory": {
                    "type": "button",
                    "theme": "primary",
                    "text": {"type": "plain-text", "content": "详细信息"},
                    "value": "{commit_url}",
                    "click": "link",
                },
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "image",
                        "src": "https://github.githubassets.com/favicons/favicon.png",
                    },
                    {"type": "plain-text", "content": "Repo2Kook"},
                ],
            },
        ],
    }
]

issue_card = [
    {
        "type": "card",
        "theme": "secondary",
        "size": "lg",
        "modules": [
            {
                "type": "header",
                "text": {
                    "type": "plain-text",
                    "content": "⁉️ @{user} {action} Issue#{number}",
                },
            },
            {
                "type": "section",
                "text": {
                    "type": "paragraph",
                    "cols": 3,
                    "fields": [
                        {"type": "kmarkdown", "content": "**📦 仓库**\n{repository}"},
                        {"type": "kmarkdown", "content": "**🚧 状态**\n{state}"},
                        {"type": "kmarkdown", "content": "**🕒 日期**\n{time}"},
                    ],
                },
            },
            {
                "type": "section",
                "text": {"type": "kmarkdown", "content": "**🆘 标题**\n{title}"},
            },
            {
                "type": "section",
                "text": {"type": "kmarkdown", "content": "**📝 信息**\n{message}"},
                "mode": "right",
                "accessory": {
                    "type": "button",
                    "theme": "primary",
                    "text": {"type": "plain-text", "content": "详细信息"},
                    "value": "{issue_url}",
                    "click": "link",
                },
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "image",
                        "src": "https://github.githubassets.com/favicons/favicon.png",
                    },
                    {"type": "plain-text", "content": "Repo2Kook"},
                ],
            },
        ],
    }
]


issue_comment_card = [
    {
        "type": "card",
        "theme": "secondary",
        "size": "lg",
        "modules": [
            {
                "type": "header",
                "text": {
                    "type": "plain-text",
                    "content": "⁉️ @{user} {action} Issue#{number} 的评论",
                },
            },
            {
                "type": "section",
                "text": {
                    "type": "paragraph",
                    "cols": 3,
                    "fields": [
                        {"type": "kmarkdown", "content": "**📦 仓库**\n{repository}"},
                        {"type": "kmarkdown", "content": "**🚧 状态**\n{state}"},
                        {"type": "kmarkdown", "content": "**🕒 日期**\n{time}"},
                    ],
                },
            },
            {
                "type": "section",
                "text": {"type": "kmarkdown", "content": "**🆘 标题**\n{title}"},
            },
            {
                "type": "section",
                "text": {"type": "kmarkdown", "content": "**📝 信息**\n{message}"},
                "mode": "right",
                "accessory": {
                    "type": "button",
                    "theme": "primary",
                    "text": {"type": "plain-text", "content": "详细信息"},
                    "value": "{comment_url}",
                    "click": "link",
                },
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "image",
                        "src": "https://github.githubassets.com/favicons/favicon.png",
                    },
                    {"type": "plain-text", "content": "Repo2Kook"},
                ],
            },
        ],
    }
]


pull_request_card = [
    {
        "type": "card",
        "theme": "secondary",
        "size": "lg",
        "modules": [
            {
                "type": "header",
                "text": {
                    "type": "plain-text",
                    "content": "⬆️ @{user} {action} PR#{number}",
                },
            },
            {
                "type": "section",
                "text": {
                    "type": "paragraph",
                    "cols": 3,
                    "fields": [
                        {"type": "kmarkdown", "content": "**📦 仓库**\n{repository}"},
                        {"type": "kmarkdown", "content": "**🚧 状态**\n{state}"},
                        {"type": "kmarkdown", "content": "**🕒 日期**\n{time}"},
                    ],
                },
            },
            {
                "type": "section",
                "text": {"type": "kmarkdown", "content": "**🆘 标题**\n{title}"},
            },
            {
                "type": "section",
                "text": {
                    "type": "kmarkdown",
                    "content": "**📝 信息**\n基分支：{base}\n目标分支：{head}\n",
                },
                "mode": "right",
                "accessory": {
                    "type": "button",
                    "theme": "primary",
                    "text": {"type": "plain-text", "content": "详细信息"},
                    "value": "{pr_url}",
                    "click": "link",
                },
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "image",
                        "src": "https://github.githubassets.com/favicons/favicon.png",
                    },
                    {"type": "plain-text", "content": "Repo2Kook"},
                ],
            },
        ],
    }
]
