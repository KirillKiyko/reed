from pyfcm import FCMNotification


def push_notification(ids, title):

    push_service = FCMNotification(api_key="AAAAdpVL-5c:APA91bEDD2-kJOVZfkLGo3KoYRiK6VnuLijl2e4R8nDfFifq-ylLTksK4Sc1DNnS-UjFeGHINoWxpD24HxYnF9-i8DfSfUKKDiP8NtgcWbMQV9Igvt5fTO9LTGjeVEjXJvYPLaPYjm1m")

    registration_ids = ids

    message_title = "Reed"

    message_body = title

    result = push_service.notify_multiple_devices(registration_ids=registration_ids, message_title=message_title, message_body=message_body)

    return result