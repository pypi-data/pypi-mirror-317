# itmgr
An import manager that allow you to manage easily your importations in your project

 # Installation
 You can install it using pip:
 ```
 pip install itmgr
 ```

# Usage
```python
from itmgr import * #Or use : install_and_import, importation, install, uninstall, remove_module, check_latest_version

# And write your importations and your code below

# Example :

install_and_import(("os", True, False, False)) # Import os module as an "import os" statement without an update check

importation(("PIL.Image", True, "Image", False)) # Import PIL.Image module as an "from PIL import Image as Image" statement without an update check

if not os.path.exists("image.png"): # Check if the image.png file exists
    Image.new("RGB", (100, 100), (255, 255, 255)).save("image.png") # Create a new image and save it as image.png

Image.open("image.png").show() # Open the image.png file
```

You can also add link between libs for importation and installations by using this line in your console : 
```bash
itmgr add lib_name link_to_install
```

You can of course delete a link by using this line in your console :
```bash
itmgr del link1 *or* itmgr del link2
```
- *link1* and *link2* are the links you want to delete


You can of course use these functions in your code :
```python
from itmgr import add, delete # delete function in code is link to del function in console for itmgr
add(lib_name, link_to_install)
delete(link1 *or* link2)
```


**Note : Please avoid using the \_\_check_latest_version\_\_ function, it is a special function used in the code that was not created for user use.** 

# Contributing
The contributions are welcome ! You can contribute by adding new features, fixing bugs, improving the documentation and code, etc.

# Author
- [ȻλƧṨʆʃłคи](https://github.com/Cassssian)