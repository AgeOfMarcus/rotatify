import streamlit as st
from PIL import Image
from io import BytesIO

@st.cache
def make_it_spin(img, inc=10, speed=33):
    # build sequence (from @turbio/rotatify)
    img = img.convert(mode="RGBA")
    sequence = []
    for rot in range(0, 360, inc):
        rotated = Image.new("RGBA", img.size, color=(255, 255, 255, 255))
        rotated = Image.alpha_composite(rotated, img.rotate(rot))
        sequence.append(rotated)
    
    # return image
    imfile = BytesIO()
    sequence[0].save(
        imfile,
        format="GIF",
        save_all=True,
        append_images=sequence[1:],
        loop=0,
        duration=speed,
    )
    imfile.seek(0)
    return Image.open(imfile)

st.title('Rotatify')
st.write('Turn any static image into a rotating gif ([source code](https://github.com/AgeOfMarcus/rotatify)).')

with st.form('image_upload'):
    image_file = st.file_uploader('Image', type=['png', 'jpg', 'jpeg'])
    increment = st.slider('Increment', min_value=0, max_value=360, value=10)
    duration = st.slider('Duration', min_value=1, value=33)
    submitted = st.form_submit_button('Rotatify')

    if submitted:
        if image_file:
            img = Image.open(image_file)
            res = make_it_spin(img, inc=increment, speed=duration)
            st.image(res)
        st.error('No image provided')
