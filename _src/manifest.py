# -*- coding: utf-8 -*-
"""
Single source of truth for the Microservices Patterns course.

UNITS      = the ~25 content partials (one HTML fragment each in _src/content/).
CATEGORIES = thematic groupings (the "by-category" view).
CHAPTERS   = the book's chapters (the "by-chapter" view).

Every one of the ~44 patterns in Chris Richardson's "Microservices Patterns"
is listed in some unit's `patterns` field, so the build can verify full coverage.
"""

COURSE_TITLE = "Microservices Patterns"
COURSE_SUBTITLE = "An architect's field guide — every pattern from Chris Richardson's book, taught with diagrams, use cases & modern tooling"

# ---------------------------------------------------------------------------
# CATEGORIES  (by-category view)  -- order defines sidebar/index ordering
# ---------------------------------------------------------------------------
CATEGORIES = [
    ("application-architecture", "Application Architecture",
     "The two ends of the spectrum — the monolith and the microservice architecture — and how to choose."),
    ("decomposition", "Decomposition Strategies",
     "How to slice a system into services along business capabilities and DDD subdomains."),
    ("communication", "Communication Styles",
     "How services talk: synchronous RPI (REST/gRPC) and asynchronous messaging."),
    ("reliability", "Reliable Communication",
     "Keeping the system up when a dependency is slow or down — the circuit breaker and friends."),
    ("service-discovery", "Service Discovery",
     "Finding the network location of service instances in a dynamic, ever-changing fleet."),
    ("transactional-messaging", "Transactional Messaging",
     "Publishing messages reliably as part of a database transaction (outbox, CDC, log tailing)."),
    ("data-consistency", "Data Consistency",
     "Maintaining consistency across services without distributed transactions — the Saga pattern."),
    ("business-logic", "Business Logic Design",
     "Organising domain logic with transaction scripts, domain models, aggregates and domain events."),
    ("querying", "Querying",
     "Answering queries that span services: API composition and CQRS read models."),
    ("external-api", "External API",
     "Giving clients a clean front door — the API gateway and backends-for-frontends."),
    ("testing", "Testing",
     "Testing services in isolation and trusting their integrations — contract & component tests."),
    ("security", "Security",
     "Authenticating and authorising requests across a service graph with access tokens."),
    ("cross-cutting", "Cross-Cutting Concerns",
     "Concerns every service shares: externalised configuration and the microservice chassis."),
    ("observability", "Observability",
     "Understanding a running system: health checks, logs, metrics, tracing, exceptions, audit."),
    ("deployment", "Deployment",
     "Packaging and running services: containers, Kubernetes, serverless, service mesh & sidecars."),
    ("refactoring", "Refactoring to Microservices",
     "Escaping the monolith incrementally with the strangler application and anti-corruption layer."),
]

# ---------------------------------------------------------------------------
# CHAPTERS  (by-chapter view)  -- mirrors the book's narrative arc
# (chapters 9 & 10 are both "Testing", merged into one page)
# ---------------------------------------------------------------------------
CHAPTERS = [
    (1,  "Escaping Monolithic Hell",
     "Why teams outgrow the monolith, the scale cube, and what the microservice architecture really is."),
    (2,  "Decomposition Strategies",
     "Defining a microservice architecture by business capability and by DDD subdomain."),
    (3,  "Interprocess Communication",
     "Synchronous RPI, asynchronous messaging, circuit breakers, service discovery and reliable messaging."),
    (4,  "Managing Transactions with Sagas",
     "Replacing distributed transactions with choreography- and orchestration-based sagas."),
    (5,  "Designing Business Logic",
     "Transaction script vs domain model, DDD aggregates, and publishing domain events."),
    (6,  "Developing Business Logic with Event Sourcing",
     "Persisting aggregates as a sequence of events — the event store, snapshots and replay."),
    (7,  "Implementing Queries",
     "Querying across services with API composition and CQRS materialised views."),
    (8,  "External API Patterns",
     "The API gateway and backends-for-frontends; GraphQL as a modern realisation."),
    (9,  "Testing Microservices (Parts 1 & 2)",
     "The test pyramid, consumer-driven contract tests, and service component tests."),
    (11, "Developing Production-Ready Services",
     "Security with access tokens, externalised configuration, observability and the chassis."),
    (12, "Deploying Microservices",
     "Language packages, VMs, containers/Kubernetes, serverless, and the service mesh / sidecar."),
    (13, "Refactoring to Microservices",
     "Strangling the monolith and protecting new services with an anti-corruption layer."),
]

# ---------------------------------------------------------------------------
# UNITS  (by-pattern view)  -- the actual content fragments
#   slug, title, category, chapter, difficulty, icon, summary, [book patterns]
# ---------------------------------------------------------------------------
UNITS = [
    dict(slug="monolith-vs-microservices",
         title="Monolith vs. Microservice Architecture",
         category="application-architecture", chapter=1,
         difficulty="Intro", icon="\U0001F3DB️",
         summary="The monolithic and microservice architectural styles, the scale cube, and when each one wins.",
         patterns=["Monolithic architecture", "Microservice architecture"]),

    dict(slug="decompose-by-business-capability",
         title="Decompose by Business Capability",
         category="decomposition", chapter=2,
         difficulty="Core", icon="\U0001F9E9",
         summary="Define services around what the business does — stable capabilities, not technical layers.",
         patterns=["Decompose by business capability"]),

    dict(slug="decompose-by-subdomain",
         title="Decompose by Subdomain (DDD)",
         category="decomposition", chapter=2,
         difficulty="Core", icon="\U0001F5FA️",
         summary="Use Domain-Driven Design subdomains and bounded contexts to find service boundaries.",
         patterns=["Decompose by subdomain"]),

    dict(slug="rpi",
         title="Remote Procedure Invocation (REST & gRPC)",
         category="communication", chapter=3,
         difficulty="Core", icon="\U0001F517",
         summary="Synchronous request/response between services using REST or gRPC — and its availability cost.",
         patterns=["Remote procedure invocation"]),

    dict(slug="messaging",
         title="Asynchronous Messaging",
         category="communication", chapter=3,
         difficulty="Core", icon="\U0001F4EC",
         summary="Decouple services with a message broker; improve availability with event-driven communication.",
         patterns=["Messaging"]),

    dict(slug="circuit-breaker",
         title="Circuit Breaker",
         category="reliability", chapter=3,
         difficulty="Core", icon="⚡",
         summary="Stop calling a failing dependency to prevent cascading failures — fail fast and recover.",
         patterns=["Circuit breaker"]),

    dict(slug="service-discovery",
         title="Service Discovery",
         category="service-discovery", chapter=3,
         difficulty="Core", icon="\U0001F9ED",
         summary="Locate service instances dynamically — client-side, server-side, self- and 3rd-party registration.",
         patterns=["Self registration", "Client-side discovery", "Server-side discovery", "3rd party registration"]),

    dict(slug="transactional-messaging",
         title="Transactional Messaging (Outbox & CDC)",
         category="transactional-messaging", chapter=3,
         difficulty="Advanced", icon="\U0001F4E4",
         summary="Atomically update the database and publish a message — the transactional outbox, polling publisher and log tailing.",
         patterns=["Transactional outbox", "Polling publisher", "Transaction log tailing"]),

    dict(slug="saga",
         title="Saga",
         category="data-consistency", chapter=4,
         difficulty="Advanced", icon="\U0001F501",
         summary="Maintain data consistency across services with a sequence of local transactions and compensations.",
         patterns=["Saga"]),

    dict(slug="business-logic",
         title="Business Logic: Domain Model & Aggregate",
         category="business-logic", chapter=5,
         difficulty="Core", icon="\U0001F9E0",
         summary="Organise domain logic: transaction script vs domain model, and DDD aggregates as consistency boundaries.",
         patterns=["Transaction script", "Domain model", "Aggregate"]),

    dict(slug="domain-event",
         title="Domain Event",
         category="business-logic", chapter=5,
         difficulty="Core", icon="\U0001F4E2",
         summary="Publish an event whenever an aggregate changes state, so other services and views can react.",
         patterns=["Domain event"]),

    dict(slug="event-sourcing",
         title="Event Sourcing",
         category="business-logic", chapter=6,
         difficulty="Advanced", icon="\U0001F4DC",
         summary="Persist an aggregate as the full sequence of events that changed it — the event store and replay.",
         patterns=["Event sourcing"]),

    dict(slug="api-composition",
         title="API Composition",
         category="querying", chapter=7,
         difficulty="Core", icon="\U0001F9F0",
         summary="Answer a cross-service query by invoking several services and joining the results in memory.",
         patterns=["API composition"]),

    dict(slug="cqrs",
         title="CQRS",
         category="querying", chapter=7,
         difficulty="Advanced", icon="\U0001F50D",
         summary="Separate the write model from purpose-built read models (materialised views) kept current by events.",
         patterns=["Command query responsibility segregation (CQRS)"]),

    dict(slug="api-gateway",
         title="API Gateway",
         category="external-api", chapter=8,
         difficulty="Core", icon="\U0001F6AA",
         summary="A single entry point that routes, aggregates and offloads cross-cutting concerns for external clients.",
         patterns=["API gateway"]),

    dict(slug="bff",
         title="Backends for Frontends (BFF)",
         category="external-api", chapter=8,
         difficulty="Core", icon="\U0001F4F1",
         summary="A dedicated API gateway per client type, owned by the front-end team — mobile, web, partner.",
         patterns=["Backends for frontends"]),

    dict(slug="contract-testing",
         title="Contract & Component Testing",
         category="testing", chapter=9,
         difficulty="Core", icon="\U0001F9EA",
         summary="Trust integrations without slow end-to-end tests — consumer-driven contracts and component tests.",
         patterns=["Consumer-driven contract test", "Consumer-side contract test", "Service component test"]),

    dict(slug="security-access-token",
         title="Microservice Security & Access Token",
         category="security", chapter=11,
         difficulty="Core", icon="\U0001F510",
         summary="Authenticate at the edge and pass a signed access token (JWT/OAuth2/OIDC) through the service graph.",
         patterns=["Access token"]),

    dict(slug="externalized-configuration",
         title="Externalized Configuration",
         category="cross-cutting", chapter=11,
         difficulty="Intro", icon="⚙️",
         summary="Supply configuration (endpoints, credentials) to a service at runtime — push and pull models.",
         patterns=["Externalized configuration"]),

    dict(slug="observability",
         title="Observability",
         category="observability", chapter=11,
         difficulty="Core", icon="\U0001F4E1",
         summary="Understand a running system: health checks, log aggregation, metrics, tracing, exceptions and audit.",
         patterns=["Health check API", "Log aggregation", "Distributed tracing",
                   "Application metrics", "Exception tracking", "Audit logging"]),

    dict(slug="microservice-chassis",
         title="Microservice Chassis",
         category="cross-cutting", chapter=11,
         difficulty="Intro", icon="\U0001F6E0️",
         summary="A framework that handles cross-cutting concerns so each new service starts production-ready.",
         patterns=["Microservice chassis"]),

    dict(slug="service-mesh-sidecar",
         title="Service Mesh & Sidecar",
         category="deployment", chapter=12,
         difficulty="Advanced", icon="\U0001F578️",
         summary="Move networking, security and observability into infrastructure with sidecar proxies and a mesh.",
         patterns=["Service mesh", "Sidecar"]),

    dict(slug="deployment-patterns",
         title="Deployment: Containers, Kubernetes & Serverless",
         category="deployment", chapter=12,
         difficulty="Core", icon="\U0001F4E6",
         summary="Four ways to run a service: language package, VM, container/Kubernetes, and serverless functions.",
         patterns=["Deploy a service as a container", "Deploy a service as a VM",
                   "Language-specific packaging format", "Serverless deployment"]),

    dict(slug="strangler-application",
         title="Strangler Application",
         category="refactoring", chapter=13,
         difficulty="Core", icon="\U0001F33F",
         summary="Migrate a monolith to microservices incrementally by routing slices of traffic to new services.",
         patterns=["Strangler application"]),

    dict(slug="anti-corruption-layer",
         title="Anti-Corruption Layer",
         category="refactoring", chapter=13,
         difficulty="Core", icon="\U0001F6E1️",
         summary="Translate between a new clean model and a legacy one so the legacy design can't leak in.",
         patterns=["Anti-corruption layer"]),
]


def all_patterns():
    """Flat, de-duplicated list of every book pattern covered (for coverage checks)."""
    seen, out = set(), []
    for u in UNITS:
        for p in u["patterns"]:
            if p not in seen:
                seen.add(p)
                out.append(p)
    return out


def category_title(slug):
    for s, t, _ in CATEGORIES:
        if s == slug:
            return t
    return slug


def category_desc(slug):
    for s, _, d in CATEGORIES:
        if s == slug:
            return d
    return ""


def units_in_category(slug):
    return [u for u in UNITS if u["category"] == slug]


def units_in_chapter(num):
    return [u for u in UNITS if u["chapter"] == num]


if __name__ == "__main__":
    ps = all_patterns()
    print("Units:      %d" % len(UNITS))
    print("Categories: %d" % len(CATEGORIES))
    print("Chapters:   %d" % len(CHAPTERS))
    print("Patterns:   %d" % len(ps))
    for p in ps:
        print("  -", p)
