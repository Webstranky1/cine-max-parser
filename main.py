from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/parse', methods=['POST'])
def parse_film():
    data = request.json
    url = data.get('url')

    if not url:
        return jsonify({'error': 'Missing URL'}), 400

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    try:
        title = soup.find('h1').text.strip()
        description = soup.find('div', class_='movie-description').text.strip()
        image = soup.find('div', class_='movie-poster').find('img')['src']
        premiere = soup.find(text="Dátum premiéry").find_next().text.strip()

        return jsonify({
            'title': title,
            'description': description,
            'image': image,
            'premiere': premiere,
            'source': url
        })

    except Exception as e:
        return jsonify({'error': f'Parsing failed: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
