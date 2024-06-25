import streamlit as st
import tensorflow as tf

# Title
st.title('Predicting Your Age')

# What is your actual age?
actual_age = st.number_input('What is your actual age?', min_value=0, max_value=100, value=30)

# What is your country's legal drinking age?
drinking_age = st.number_input('What is the legal drinking age?', min_value=0, max_value=100, value=21)

# Load the model
model = tf.keras.models.load_model('models/age_prediction_model.h5')

# Upload the image
uploaded_file = st.file_uploader('Choose an image...', type=['jpg', 'png'])

# If the image is uploaded
if uploaded_file is not None:
    # Read the image
    img = tf.io.decode_image(uploaded_file.getvalue(), channels=3)
    img = tf.image.resize(img, [224, 224])
    img = img / 255.0
    img = np.expand_dims(img, axis=0)

    # Predict the age
    age = round(model.predict(img)[0][0])

    # Display the image
    st.image(uploaded_file, use_column_width=True)

    # Display the predicted age in the side bar
    st.sidebar.markdown(f'Predicted Age: {age}')

    # Display the difference with font colors in the sidebar
    if actual_age > age:
        st.sidebar.markdown(f'<p style="color:green;">You are {actual_age - age} years younger than you look.</p>', unsafe_allow_html=True)
    elif actual_age < age:
        st.sidebar.markdown(f'<p style="color:red;">You are {age - actual_age} years older than you look.</p>', unsafe_allow_html=True)
    else:
        st.sidebar.write('Your predicted age matches your actual age.')

    # Display the legal difference in the sidebar
    if drinking_age < age:
        st.sidebar.markdown(f'<p style="color:green;">You look like you are {abs(drinking_age - age)} years older than the legal drinking age.</p>', unsafe_allow_html=True)
    elif drinking_age > age:
        st.sidebar.markdown(f'<p style="color:red;">You look like you are {abs(age - drinking_age)} years younger than the legal drinking age.</p>', unsafe_allow_html=True)
    else:
        st.sidebar.write('Your predicted age matches the legal drinking age.')
        
# Display the bottom of the page
st.write('---')
st.write('Made with ❤️ by [p0kes](https://github.com/danp0kes)')

    

