from firebase_admin import messaging


def send_to_token():
    # [START send_to_token]
    # This registration token comes from the client FCM SDKs.
    registration_token = "dXOYsxcST_K6IMcRhilE9H:APA91bFe6LvOpGJPdm8LUi0TmwCVMykoGFWgCnpkjG0MSRqyqACrqTaxjLoVFE0O5UfZ7GG5p-7oQkkQS7CgYUQCnECxy5UPOwqXBbcQmvmbQ7xIU90lsjUfv_j_DfT4hr-uTnIhcZ-Z"
    # registration_token = "d1LWJJVqeGjdd3Ntn3iwTn:APA91bGdsmIu7_GaCTHxuAOdEQ69S5DUZWbaP3TKbC6KvbOQOdKEQvWjMVs_nUcCkj2y7FnUjZ4_QOJsNsIsyFfcf_D7QY4WqF6jXr4D2Ym5e48jLQnnRYvXdKKaQEjLkrbAOMnxmMfW"

    # See documentation on defining a message payload.
    message = messaging.Message(
        data={
            "score": "850",
            "time": "2:45",
        },
        notification=messaging.Notification(
            title="Shali",
            body="This is a notification that will be displayed if your app is in the background.",
        ),
        token=registration_token,
    )

    # Send a message to the device corresponding to the provided
    # registration token.
    response = messaging.send(message)
    # Response is a message ID string.
    print("Successfully sent message:", response)
    # [END send_to_token]


# init_firestore_client()
import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("../shali-7e651-firebase-adminsdk-himas-ca3e05a04e.json")
firebase_admin.initialize_app(cred)

send_to_token()
