def create_chunks(transcript, chunk_size=1000, chunk_overlap=200):
    """
    Convert transcript segments into overlapping text chunks
    while preserving timestamp information.
    """

    chunks = []

    current_text = []
    current_start = None
    current_end = None
    current_length = 0

    for segment in transcript:

        text = segment["text"].strip()

        if not text:
            continue

        start = segment["start"]
        end = start + segment["duration"]

        # Start a new chunk
        if current_start is None:
            current_start = start

        current_text.append(text)
        current_length += len(text)
        current_end = end

        # Chunk is large enough
        if current_length >= chunk_size:

            chunks.append({
                "text": " ".join(current_text),
                "start": current_start,
                "end": current_end
            })

            # Keep the last part for overlap
            overlap_text = []
            overlap_length = 0

            for previous_text in reversed(current_text):

                if overlap_length + len(previous_text) > chunk_overlap:
                    break

                overlap_text.insert(0, previous_text)
                overlap_length += len(previous_text)

            current_text = overlap_text
            current_length = overlap_length

            if current_text:
                # Approximate start of the overlapping section
                current_start = current_end
            else:
                current_start = None

    # Add remaining text
    if current_text:

        chunks.append({
            "text": " ".join(current_text),
            "start": current_start,
            "end": current_end
        })

    return chunks