# Preprocessign an Image

The main objective of the Preprocessing phase is to make as easy as possible for the OCR system to distinguish a character/word from the background. There are several techniques used for Preprocessing but this **Preprocessor** class can do it without you going into details and jargon of traditional methods.

`!pip install -U ocred -q`

```
# manually preprocessing an image
import cv2
from scipy import ndimage
from ocred import Preprocessor
from google.colab.patches import cv2_imshow


preprocessed = Preprocessor("/content/images/CosmosOne.jpg")
```

```
# scan the image and copy the scanned image
scanned = preprocessed.scan()

cv2_imshow(scanned)
```

![image](https://user-images.githubusercontent.com/82112540/184899616-2a418f9b-ad82-4bf4-92b7-98a96126dbd1.png)

```
# remove noise
noise_free = preprocessed.remove_noise(overriden_image=scanned)

cv2_imshow(noise_free)
```

![image](https://user-images.githubusercontent.com/82112540/184900366-34551949-42f7-4b6c-b448-8a0a6fb05779.png)

```
# thicken the ink to draw Hough lines better
thickened = preprocessed.thicken_font(overriden_image=noise_free)

cv2_imshow(thickened)
```

![image](https://user-images.githubusercontent.com/82112540/184900996-2eec35d6-ef00-4fc1-bd8d-34944c793b0e.png)

```
# calculate the median angle of all the Hough lines
_, median_angle = preprocessed.rotate(
    inplace=True, overriden_image=thickened
)

cv2_imshow(_)
```

![image](https://user-images.githubusercontent.com/82112540/184901244-741ea02d-06de-4d39-a9a1-ce04c2eabf91.png)

```
# rotate the original scanned image
rotated = ndimage.rotate(orig, median_angle)

cv2_imshow(rotated)
```

![image](https://user-images.githubusercontent.com/82112540/184902055-61c50a47-7894-4d2d-aba7-89acfa4b53f1.png)

```
# remove noise again
final_img = preprocessed.remove_noise(inplace=True, overriden_image=rotated)

cv2_imshow(final_img)
```

![image](https://user-images.githubusercontent.com/82112540/184902140-42582eac-e765-44b6-b518-b8aa81ada09c.png)
