# app.py

import streamlit as st
import numpy as np
import pandas as pd
import librosa
import plotly.express as px
from pydub import AudioSegment

def main():
    st.title("Audio Feature Analysis")

    modality_options = ["Videos", "Learning Design", "Pre", "Post"]
    selected_modalities = st.multiselect("Select Modalities", modality_options)

    if "Videos" in selected_modalities:
        num_videos = st.number_input("Number of Videos to Upload", min_value=1, max_value=10, value=1, step=1)

        uploaded_files = st.file_uploader("Upload Video(s)", type=["mp4", "mov"], accept_multiple_files=True)

        if uploaded_files:
            st.write("Videos Uploaded!")

            for i, file in enumerate(uploaded_files):
                st.video(file, format="video/mp4", start_time=0)

                # Convert video to audio
                audio = convert_video_to_audio(file)

                # Calculate audio features
                audio_features = calculate_audio_features(audio)

                # Display audio features
                st.subheader(f"Audio Features - Video {i + 1}")
                st.write(audio_features)

                # Display audio heatmap
                st.subheader(f"Audio Heatmap - Video {i + 1}")
                plot_audio_heatmap(audio)

def convert_video_to_audio(video_file):
    st.write("Converting video to audio...")
    audio = AudioSegment.from_file(video_file, format="mp4")
    return audio



def calculate_audio_features(audio):
    st.write("Calculating audio features...")

    # Convert audio to numpy array
    samples = np.array(audio.get_array_of_samples())

    # Get sample rate
    sample_rate = audio.frame_rate

    # Calculate pitch using librosa
    pitches, magnitudes = librosa.core.pitch.piptrack(y=samples.astype(float), sr=sample_rate)
    pitch = np.max(pitches)

    # Calculate duration in seconds
    duration = len(samples) / sample_rate

    # Calculate tone (you can customize this based on your definition of tone)
    tone = "Major" if pitch > 0 else "Minor"

    # Calculate total frequency
    total_frequency = np.sum(np.abs(librosa.stft(y=samples.astype(float))))

    # Display the results
    st.subheader("Audio Features")
    st.write(f"Total Frequency: {total_frequency:.2f} Hz")
    st.write(f"Pitch: {pitch:.2f}")
    st.write(f"Tone: {tone}")
    st.write(f"Duration: {duration:.2f} seconds")

    # Plot graphs
    st.subheader("Graphs")

    # Plot Total Frequency
    st.subheader("Total Frequency")
    time_values = np.arange(len(samples)) / sample_rate
    fig_total_frequency = px.line(x=time_values, y=np.abs(librosa.stft(y=samples.astype(float))), labels={'x': 'Time', 'y': 'Amplitude'})
    st.plotly_chart(fig_total_frequency)

    # Plot Pitch
    st.subheader("Pitch")
    fig_pitch = px.line(x=time_values, y=pitches[0], labels={'x': 'Time', 'y': 'Pitch'})
    st.plotly_chart(fig_pitch)

    # Plot Tone
    st.subheader("Tone")
    # Add your custom tone visualization here, as it's not clear how you want to visualize tone in the graph

    return total_frequency, pitch, tone, duration


def plot_audio_heatmap(audio):
    st.write("Generating audio heatmap...")
    samples = np.array(audio.get_array_of_samples())
    sample_rate = audio.frame_rate

    # Use librosa to generate a spectrogram
    Sxx = np.abs(librosa.stft(y=samples.astype(float)))  # Remove 'sr' argument and take the magnitude

    Sxx_db = librosa.amplitude_to_db(Sxx, ref=np.max)

    # Create a heatmap using Plotly
    fig = px.imshow(Sxx_db, aspect='auto', labels=dict(x='Time', y='Frequency (Hz)'), color_continuous_scale='Viridis')
    st.plotly_chart(fig)

if __name__ == "__main__":
    main()