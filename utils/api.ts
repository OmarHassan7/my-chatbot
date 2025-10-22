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
  endpoint: string = "/api/chat"
): Promise<ChatResponse> => {
  console.log("🚀 Sending message to:", endpoint);
  console.log("📝 Message:", message);

  try {
    // Ensure we have a proper base URL for production
    const baseUrl = typeof window !== "undefined" ? window.location.origin : "";
    const fullUrl = endpoint.startsWith("http")
      ? endpoint
      : `${baseUrl}${endpoint}`;

    console.log("🌐 Full URL:", fullUrl);

    const response = await fetch(fullUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message }),
    });

    console.log("📊 Response status:", response.status);
    console.log(
      "📊 Response headers:",
      Object.fromEntries(response.headers.entries())
    );

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

export const checkApiStatus = async (
  endpoint: string = "/api"
): Promise<any> => {
  const baseUrl = typeof window !== "undefined" ? window.location.origin : "";
  const fullUrl = endpoint.startsWith("http")
    ? endpoint
    : `${baseUrl}${endpoint}`;

  const response = await fetch(fullUrl);

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  return response.json();
};
