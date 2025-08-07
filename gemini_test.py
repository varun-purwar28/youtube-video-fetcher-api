# import google.generativeai as genai

# genai.configure(api_key="AIzaSyBbrNRJj4qY0SmuBfGVjUFbQO-Q3ranFyI")

# model = genai.GenerativeModel('gemini-pro')
# response = model.generate_content("Hello Gemini, how are you?")
# print(response.text)

# filepath: c:\Users\hp\Desktop\Gemini\gemini_test.py
import google.generativeai as genai

genai.configure(api_key="AIzaSyBbrNRJj4qY0SmuBfGVjUFbQO-Q3ranFyI")

def main():
  """Initializes the model and generates content."""
  model = genai.GenerativeModel('gemini-1.5-flash-latest')
  prompt = "Write a short, futuristic story about a programmer and their AI assistant."
  print(f"Sending prompt: {prompt}\n")
  response = model.generate_content(prompt)
  print("--- Gemini's Response ---")
  print(response.text)

if __name__ == "__main__":
  main()