import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

# if main, run the code
if __name__ == '__main__':
    
    # Load data
    df = pd.read_csv('python/predictions.csv')
    
    # Title
    st.title('Age Verification - Summary')
    
    # Create Subheader for Dataset
    st.header('Data - Age Distribution of Photos')
    
    # Show picture of the data
    st.image('./pics/age_distributions.png', use_column_width=True)
    
    # Create sub-header
    st.header('Test Set Results')
    
    # Create histogram of actual and predicted values
    fig = px.histogram(df, x=['actual','predicted'], nbins=100, title='Actual vs Predicted Values', color_discrete_sequence=['hotpink', 'aqua'], barmode='overlay')

    # Make it dark theme
    fig.update_layout(template='plotly_dark')
    
    # Show plot
    st.plotly_chart(fig)
    
    # Create the histogram
    fig = px.histogram(df, 
                    x='difference', 
                    title='Difference between Actual and Predicted Values', 
                    color_discrete_sequence=['aqua','hotpink'],
                    histnorm='percent')

    # Save legend title
    fig.update_layout(legend_title_text='Over 21')

    # Apply dark theme
    fig.update_layout(template='plotly_dark')

    # Show the figure
    st.plotly_chart(fig)

    # Create plot
    fig = go.Figure()

    # Round down the predicted ages
    df['predicted_rounded_down'] = np.floor(df['predicted'])

    # Filter data into two groups
    df_over_21 = df[df['actual'] > 20]
    df_under_21 = df[df['actual'] <= 20]

    # Function to calculate the CDF
    def calculate_cdf(data):
        sorted_data = np.sort(data)
        cdf = np.arange(1, len(sorted_data) + 1) / len(sorted_data)
        return sorted_data, cdf

    # Calculate CDF for each group
    x_vals_over_21, y_vals_over_21 = calculate_cdf(df_over_21['predicted_rounded_down'])
    x_vals_under_21, y_vals_under_21 = calculate_cdf(df_under_21['predicted_rounded_down'])
    
    # Inititalize the figure
    fig = go.Figure()

    # Add CDF line for those over 21
    fig.add_trace(go.Scatter(x=x_vals_over_21, y=y_vals_over_21, mode='lines', line=dict(color='hotpink'), name='Over 21'))

    # Add CDF line for those under 21
    fig.add_trace(go.Scatter(x=x_vals_under_21, y=y_vals_under_21, mode='lines', line=dict(color='aqua'), name='Under 21'))

    # Add vertical line at 21
    fig.add_vline(x=21, line_dash='dash', line_color='red', annotation_text='Age 21', annotation_position='top right')

    # Set title and legend
    fig.update_layout(
        title='Cumulative Density Function of Predicted Ages',
        xaxis_title='Predicted Age',
        yaxis_title='Cumulative Density',
        legend_title='Actual Age Group',
        template='plotly_dark'
    )

    # Show plot
    st.plotly_chart(fig)
    
    # Create lists to store the accuracy over 21 and under 21
    accuracy_over_21 = []
    accuracy_under_21 = []

    for age in range(0, 21):
        # slice the dataframe to only include rows where predicted age is under 'age'
        df_slice = df[df['predicted'] <= age]
        
        # Find average of predicted under 21
        average = 1 - df_slice['over_21'].mean()

        # save the average to a list
        accuracy_under_21.append({age: average})
        
    for age in range(21, 100):  # corrected range
        # slice the dataframe to only include rows where predicted age is over 'age'
        df_slice = df[df['predicted'] > age]
        
        # Find average of predicted over 21
        average = df_slice['over_21'].mean()

        # save the average to a list
        accuracy_over_21.append({age: average})
        
    # Create plot
    fig = go.Figure()

    # Add a line plot for the accuracy over 21
    fig.add_trace(go.Scatter(x=[list(x.keys())[0] for x in accuracy_over_21],
                            y=[list(x.values())[0] for x in accuracy_over_21],
                            mode='lines',
                            name='Over 21'))

    # Add a line plot for the accuracy under 21
    fig.add_trace(go.Scatter(x=[list(x.keys())[0] for x in accuracy_under_21],
                            y=[list(x.values())[0] for x in accuracy_under_21],
                            mode='lines',
                            name='Under 21'))

    # Add horizontal line at age 21
    fig.add_shape(type="line", x0=21, y0=0, x1=21, y1=1.2, line=dict(color="black", width=2, dash="dash"))

    # Add histogram of predicted ages as a percentage with Gaussian kernel density estimation
    fig.add_trace(go.Histogram(x=df['predicted'],
                                nbinsx=100,
                                name='Ages',
                                marker_color='hotpink',
                                histnorm='probability',  # Normalize histogram to probability
                                cumulative_enabled=True,  # Enable cumulative accumulation
                                opacity=0.5,
                                marker=dict(color='rgba(0,0,0,0)')  # Make the histogram transparent
                                ))

    # Update layout
    fig.update_layout(title='Accuracy as Prediction Ages Increases',
                    xaxis_title='Distribution of Ages',
                    yaxis_title='Accuracy (%)')

    # Change to dark theme
    fig.update_layout(template='plotly_dark')

    # Show plot
    st.plotly_chart(fig)
    
    # Show header for analysis
    st.header('Analysis')
    
    # Show analysis
    st.write('''
             Those that are actually under 21 are being categorized as underage 61% of the time. This doesn't sound too great, but you have to remember the distribution of actual ages in this data set where more than half are under 30. Everybody that is predicted to be 12 and under is correctly identified as those that are under 21.

Those that are actually over 21 are being categorized as over 21 in 95% of cases. Those that are predicted to be over 40 actually are in this case too.

Using this information, 29% of users can be safely identified, when they fit within the predicted age of under 12 and over 42. However, this would need to be replicated.

Also note that most people purchasing items at a grocery store are hardly 12. Instead the median age of customers at a grocery store is estimated to be 44, according to [this source](https://adplanetads.com/spotlight/grocery-shopper-demographics-retail-dooh/#:~:text=Age%3A%20The%20average%20age%20of,their%20own%20ways%20of%20shopping.).''')
    
    # Add a link to the main page
    st.markdown('[Go back to the main page](http://localhost:8501/)')
