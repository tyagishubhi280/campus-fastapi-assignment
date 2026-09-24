# Proof of Work Screenshots

Capture these from Swagger UI at `http://127.0.0.1:8000/docs` after running the application.

Save them with these names:

1. `01_post_item.png` - successful POST /items
2. `02_get_items.png` - GET /items
3. `03_get_item_by_id.png` - GET /items/{item_id}
4. `04_put_item.png` - successful PUT /items/{item_id}
5. `05_delete_item.png` - successful DELETE /items/{item_id}
6. `06_status_filter.png` - GET /items/status/Found or Lost
7. `07_category_filter.png` - GET /items/category/Accessories
8. `08_invalid_item_validation.png` - invalid status or empty required field, showing HTTP 422
9. `09_post_event.png` - successful POST /events
10. `10_get_events.png` - GET /events
11. `11_successful_reservation.png` - successful POST /events/{event_id}/reserve
12. `12_event_reservations.png` - GET /events/{event_id}/reservations
13. `13_event_availability.png` - GET /events/{event_id}/availability
14. `14_cancel_reservation.png` - successful DELETE /reservations/{reservation_id}
15. `15_full_event_error.png` - failed reservation because the event is full, HTTP 409

Make sure the screenshots clearly show the Swagger endpoint and the response status/body.

Do not put passwords, API keys or other secrets in screenshots.
