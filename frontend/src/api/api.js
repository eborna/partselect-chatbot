
// export const getAIMessage = async (userQuery) => {

//   const message = 
//     {
//       role: "assistant",
//       content: "Connect your backend here...."
//     }

//   return message;
// };

export const getAIMessage = async (userQuery) => {
  try {
    const response = await fetch('http://127.0.0.1:5000/get-message',  {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
      body: JSON.stringify({ query: userQuery }),
    });

    if (!response.ok) {
      throw new Error('Network response was not ok');
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error:', error);
    return {
      role: "assistant",
      content: "I'm sorry, there was an error processing your request. Please try again later."
    };
  }
};