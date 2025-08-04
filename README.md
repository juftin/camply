<div align="center">
<a href="https://github.com/juftin/camply">
  <img src="https://raw.githubusercontent.com/juftin/camply/main/docs/_static/camply.svg"
    width="400" height="400" alt="camply">
</a>
</div>

**`camply`**, the campsite finder ⛺️, is a tool to help you book a campsite online. Finding
reservations at sold out campgrounds can be tough. That's where camply comes in. It searches
thousands of campgrounds across the ~~USA~~ world via the APIs of booking services like
[recreation.gov](https://recreation.gov). It continuously checks for cancellations and
availabilities to pop up - once a campsite becomes available, camply sends you a notification
to book your spot!

---

## Directory Structure

```text
📂 camply
├── LICENSE
├── README.md
└── cli
|   ├── pyproject.toml
|   ├── camply
|   └── ...
└──  frontend
|   ├── package.json
|   ├── tsconfig.json
|   ├── src
|   └── ...
└──  backend
    ├── pyproject.toml
    ├── camply
    └── ...
```

### cli

The `cli` directory contains the legacy code for `camply`, the command line interface
for the campsite finder.

### frontend

The `frontend` directory contains the code for React TypeScript frontend for the
full stack `camply` application.

### backend

The `backend` directory contains the code for the FastAPI backend for the full stack
`camply` application.
