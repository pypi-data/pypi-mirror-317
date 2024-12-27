import tempfile

from qcloud_cos import CosS3Client


def upload_cos_figures(client: CosS3Client, bucket: str, figures: list[str]) -> list[str]:
    figures_names = []
    for figure in figures:
        with tempfile.NamedTemporaryFile(delete=True, suffix=".png") as f:
            figure.save(f.name)

            file_name = f.name.split("/")[-1]
            figures_names.append(file_name)

            # upload to cos
            client.upload_file(
                Bucket=bucket,
                LocalFilePath=f.name,
                Key=f"figure-extraction/{file_name}",
            )

    return figures_names


def get_cos_figures(client: CosS3Client, bucket: str, figures: list[str]) -> list[str]:
    figures_urls = []
    for figure in figures:
        figure_url = client.get_presigned_url(
            Bucket=bucket,
            Key=f"figure-extraction/{figure}",
            Method="GET",
            Expired=3600,
        )
        figures_urls.append(figure_url)

    return figures_urls
