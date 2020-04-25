# 10slowfingers
A Chromium extension for the 10fastfingers.com or 10ff.net website, used in conjunction with the [AutoTypewriter bot](https://github.com/samuel-gamelin/AutoTypewriter).

## Installation
In your browser's extensions page, load the 10slowfingers directory using the "Load unpacked" option. You might have to enable developer settings.

## Usage
When on the [10fastfingers.com](https://10fastfingers.com) or [10ff.net](https://10ff.net) website, you can click on the extension action icon as shown below (the gray square with the 1 in it):

<img width="240" alt="Screen Shot 2020-04-25 at 11 53 45 AM" src="https://user-images.githubusercontent.com/13603771/80284296-ae6c6f80-86eb-11ea-97e0-bd213c595c73.png">

When you click this for the first time you'll be prompted to enter a [paste.ee](https://paste.ee) application key. Subsequent requests will not prompt you for a key. At this point the contents of the typying test will be upload as a paste if they can be found and an appropriate message will be output in the browser's console:

On success:

<img width="539" alt="Screen Shot 2020-04-25 at 12 00 19 PM" src="https://user-images.githubusercontent.com/13603771/80284454-90533f00-86ec-11ea-9a53-d1e74b40b902.png">

When no words can be found (notably when on the multiplayer test on 10fastfingers.com; it only works on 10ff.net):
<img width="540" alt="Screen Shot 2020-04-25 at 12 00 40 PM" src="https://user-images.githubusercontent.com/13603771/80284471-b11b9480-86ec-11ea-8d08-08a9cfb2d95b.png">

At this point you're ready to use the `autotypewriter.py` script to type out the contents of the paste using the --paste options along with other options of your liking.
