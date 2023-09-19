# PYGAME VN GENERATOR (DESKTOP APP GUI)

A Visual Novel Generator that transforms plain text into an engaging and visually interactive novel, powered by Open Source Generative AI.


## About

Visual novels are a form of digital interactive fiction that combine storytelling with visuals and audio elements. This project leverages the capabilities of open-source generative AI to turn mundane text into a visually captivating and auditory experience for users.

We've incorporated two major models into this project:

```
llama-2-13b-chat.ggmlv3.q2_K.bin
```
```
stable-diffusion-xl-base-1.0
```

Thanks to 4-bit quantized models, we can efficiently run the latest Language Model models like Llama 2 13B on GPUs with less than 16 GB VRAM.

## How to Run

Follow these steps to get started with the Pygame VN Generator:

1. Clone the GitHub repository or download it:

   ```
   git clone https://github.com/abhiram1809/VM_Game_Generator
   ```
2. Install the required libraries:
    ```
    pip install -r requirements.txt
    ```
3. Host and run the following two notebooks on a GPU instance. Ensure that both notebooks collectively use less than 30 GB of VRAM. Make sure you have an NGROK account set up for Auth tokens.

[Colab: Llama Server](https://colab.research.google.com/drive/1HhLWckttv5A6kcC64MnmXnUVckSKIZ6Z#scrollTo=4bKQIsIq-d8y)

[Colab: Stable Diffusion](https://colab.research.google.com/drive/1rR2rwZjIgVQ41nnZaJvpZcn7fPHSp35c)

4. Once the servers are up and running, add the file you want to convert into a visual novel to the main directory. By default, it will run 'The Bet.txt', you can use other formats like .docx and .pdf as well. Change the following line in VN_pygame.py to your file name and ngrok llama and SD servers:
```
colab_ngrok_url_llama = "http://de5f-34-125-218-8.ngrok-free.app"
colab_ngrok_SD = "http://87c3-34-29-116-85.ngrok-free.app/"
file_path = "The Bet.txt"
```

5. Run VN_pygame.py:

```
python VN_pygame.py
```

