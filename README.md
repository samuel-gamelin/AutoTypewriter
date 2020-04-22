# AutoTypewriter

A set of Python utilities to automatically type out text, primarily in typing competitions.

## Requirements

### General
- Python 3
- Windows

### For OCR capabilities
- Tesseract Open Source OCR
  - [Windows installers](https://github.com/UB-Mannheim/tesseract/wiki)
  - [Installers for other platforms](https://github.com/tesseract-ocr/tesseract/wiki#installation) - Currently unsupported
- Tesseract Open Source OCR trained data for non-Latin OCR
  
### For [paste.ee](https://paste.ee) functionality and [10fastfingers.com](https://10fastfingers.com)/[10ff.net](https://10ff.net) integration
- Chrome, with the [10slowfingers](https://github.com/samuel-gamelin/AutoTypewriter/tree/master/10slowfingers) extension installed
- A valid application key from [paste.ee](https://paste.ee)

## Usage

1. Clone this repository and enter the new directory
   ```
   git clone https://github.com/samuel-gamelin/AutoTypewriter && cd AutoTypewriter
   ```

2. Install the python dependencies located in the `requirements.txt` file (demonstrated here using pip3). The use of [virtualenv](https://virtualenv.pypa.io/en/latest/) is recommended.
   ```
   pip3 install -r requirements.txt
   ```

3. Run the `autotypewriter.py` script with your desired options. The following are some examples.

    Run the typewriter using OCR capabilities (this is the default behaviour, unless the --paste option is specified), making it take screenshots of the bounding box on a repeated basis each time after typing out the contents (with a 0.08s interval between each character) of a single screenshot. This will continue until the contents of the screenshots of the bounding box being taken do not change. A common use case for this scenario would be a rolling block of text. The bounding box is a rectangular area of the screen that is formed between the two points which you select by clicking with your mouse after the script commences execution.
    ```
    python3 autotypewriter.py --repeat --interval 0.08
    ```
    Run the typewriter using OCR capabilities with Vietnamese trained language data, making it take a single screenshot of the selected bounding box and typing out its contents (with a 0.08s interval between each character) followed by entering the Tab+Enter hotkey.
    ```
    python3 autotypewriter.py --interval 0.08 --lang vie --ending-type hotkey --ending-keystrokes Tab Enter
    ```
    Run the typewriter using paste.ee integration with a 0.08s interval between each character being typed out. Once the script has loaded the contents of your latest paste, which you would have submitted using the 10slowfingers Chrome extension, a message is sent to standard output and typing will begin when you perform a click.
    ```
    python3 autotypewriter.py --paste-token <your paste.ee application key> --interval 0.08
    ```
