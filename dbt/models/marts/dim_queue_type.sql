select
    queue_id,
    queue_name

from {{ ref('queue_types') }}