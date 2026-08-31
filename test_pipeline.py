from src.pipeline import YouTubeRAGPipeline


url = "https://www.youtube.com/watch?v=J5_-l7WIO_w"


# Create pipeline
pipeline = YouTubeRAGPipeline()


# Process video
info = pipeline.process_video(url)

print("\n==============================")
print("VIDEO PROCESSED")
print("==============================")

print(f"Transcript segments: {info['segments']}")
print(f"Chunks: {info['chunks']}")


# Ask question
question = "What problem are we trying to solve in this video?"

result = pipeline.ask(question)


print("\n==============================")
print("ANSWER")
print("==============================")

print(result["answer"])


print("\n==============================")
print("SOURCES")
print("==============================")

for i, source in enumerate(result["sources"], start=1):

    chunk = source["chunk"]

    print(
        f"{i}. "
        f"{chunk['start']:.2f}s - "
        f"{chunk['end']:.2f}s"
    )