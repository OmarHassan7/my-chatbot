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
  console.log("Sending message to:", endpoint);

  const response = await fetch(endpoint, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ message }),
  });

  console.log("Response status:", response.status);
  console.log("Response headers:", response.headers);

  if (!response.ok) {
    const errorText = await response.text();
    console.error("Error response:", errorText);
    throw new Error(`HTTP error! status: ${response.status} - ${errorText}`);
  }

  return response.json();
};

export const checkApiStatus = async (
  endpoint: string = "/api"
): Promise<any> => {
  const response = await fetch(endpoint);

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  return response.json();
};
