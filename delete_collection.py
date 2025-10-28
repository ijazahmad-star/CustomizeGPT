from weaviate import connect_to_weaviate_cloud
from app.config import WEAVIATE_URL, WEAVIATE_API_KEY

def reset_weaviate_collection():
    client = connect_to_weaviate_cloud(
        cluster_url=WEAVIATE_URL,
        auth_credentials=WEAVIATE_API_KEY,
    )

    try:
        # List all collections in the cluster
        collections = client.collections.list_all()
        # print("📚 Existing collections:", [c.name for c in collections])

        # Delete if "StrategisthubDocs" exists
        if "StrategisthubDocs" in collections:
            client.collections.delete("StrategisthubDocs")
            print("🗑️ Deleted 'StrategisthubDocs' collection successfully.")
        else:
            print("No existing collection named 'StrategisthubDocs' found.")
    finally:
        client.close()

if __name__ == "__main__":
    reset_weaviate_collection()