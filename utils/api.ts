interface ChatRequest {
  message: string;
  conversation_id?: string;
}

interface ChatResponse {
  response: string;
  conversation_id?: string;
}

export const sendMessage = async (
  message: string,
  endpoint: string = "http://localhost:8000"
): Promise<ChatResponse> => {
  console.log("🚀 Sending message to:", endpoint);
  console.log("📝 Message:", message);

  try {
    const response = await fetch(endpoint, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message }),
    });

    console.log("📊 Response status:", response.status);

    if (!response.ok) {
      const errorText = await response.text();
      console.error("❌ Error response:", errorText);
      throw new Error(`HTTP error! status: ${response.status} - ${errorText}`);
    }

    const data = await response.json();
    console.log("✅ Success response:", data);
    return data;
  } catch (error) {
    console.error("💥 Fetch error:", error);
    throw error;
  }
};
