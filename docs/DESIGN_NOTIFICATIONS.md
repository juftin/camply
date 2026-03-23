# DESIGN_NOTIFICATIONS: Notification Architecture

This document defines the architecture for the notification layer in `camply`, focusing on a standardized interface, multiple provider support, and asynchronous delivery.

## 🎯 Architecture Goals
1. **Standardization**: All notification channels must implement a unified `BaseNotificationProvider`.
2. **Asynchronous Delivery**: Notifications are handled by dedicated Celery tasks to avoid blocking the scanning worker.
3. **User-Centric**: Users can configure their own notification preferences and keys (e.g., Pushover user key, Webhook URL).
4. **Resilience**: Implement retries and error tracking for failed notifications.

---

## 🏗️ Core Interface: `BaseNotificationProvider`

Every notification channel must inherit from this ABC.

```python
class BaseNotificationProvider(ABC):
    @property
    @abstractmethod
    def id(self) -> str:
        """Unique slug: e.g., 'pushover', 'email', 'webhook'"""
        pass

    @abstractmethod
    async def send_alert(self, user_config: Dict[str, Any], payload: NotificationDTO) -> None:
        """
        Deliver the notification to the user using their specific configuration.
        """
        pass
```

---

## 📦 The Unified DTO: `NotificationDTO`

The data structure sent to the notification providers.

- `title`: `String` (e.g., "Campsite Available: Yosemite")
- `message`: `String` (Detailed description including dates and site info)
- `booking_url`: `String` (Direct link to book)
- `park_name`: `String`
- `campsite_name`: `String`
- `start_date`: `Date`
- `end_date`: `Date`
- `metadata`: `Dict[String, Any]` (Provider-specific raw attributes)

---

## 🚀 Notification Workflow

### 1. Detection
The **Smart Poller** identifies a match between a `ScanResult` and a `UserScan`.

### 2. Dispatch
The worker enqueues a Celery task: `send_notification_task(user_id, notification_dto)`.

### 3. Delivery
The `send_notification_task` does the following:
1. Fetches the user's `pushover_token` or other configured provider keys from the DB.
2. Selects the appropriate `BaseNotificationProvider`.
3. Calls `provider.send_alert(user_config, notification_dto)`.
4. Logs the delivery status in a `notification_history` table (Optional/Future).

---

## 🛠️ Supported Providers (Roadmap)

1. **Pushover (MVP)**:
   - *Config*: `user_key`
   - *Status*: High Priority
2. **Webhooks**:
   - *Config*: `webhook_url`
   - *Status*: High Priority (Discord, Slack, etc.)
3. **Email (SMTP)**:
   - *Config*: `email_address`
   - *Status*: Medium Priority
4. **Apprise**:
   - *Config*: `email_address`
   - *Status*: Medium Priority (Universal wrapper for 50+ services)
5. **Ntfy**:
   - *Config*: `topic_url`
   - *Status*: Medium Priority

---

## 🔒 Security & Performance
- **Secrets Management**: User notification tokens must be handled securely in the database.
- **Rate Limiting**: Implementation of provider-specific rate limiting (e.g., Twilio/SMS limits) to prevent excessive costs or API bans.
- **Failover**: If a primary notification method fails, we can optionally fall back to a secondary method if configured.
