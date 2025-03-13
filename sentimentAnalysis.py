import json
from transformers import pipeline
import matplotlib.pyplot as plt
# BERT duygu analizi modeli yükleme
sentiment_analyzer = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english",
    truncation=True,
    padding=True,
    max_length=512
)

# JSON dosyasından verileri okuma
def load_comments_from_json(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        data = json.load(f)
    # String yorumları sözlük formatına çevir
    if isinstance(data, list) and isinstance(data[0], str):
        data = [{"comment": comment} for comment in data]
    return data

# Uzun yorumları parçalama
def split_comment(comment, max_length=512):
    tokens = comment.split()  # Kelime bazlı bölüyoruz
    chunks = [' '.join(tokens[i:i + max_length]) for i in range(0, len(tokens), max_length)]
    return chunks

# Yorumlara duygu analizi uygulama
def analyze_sentiment(data):
    for item in data:
        comment = item.get("comment")
        if comment:
            try:
                # Yorum uzun ise parçala
                chunks = split_comment(comment)
                sentiments = []
                scores = []
                
                for chunk in chunks:
                    result = sentiment_analyzer(chunk)[0]
                    sentiments.append(result["label"])
                    scores.append(result["score"])

                # Çoğunluk duygu sonucu belirle
                sentiment = max(set(sentiments), key=sentiments.count)
                avg_score = sum(scores) / len(scores)  # Skorların ortalamasını al
                
                item["sentiment"] = sentiment
                item["score"] = avg_score
            except Exception as e:
                print(f"Yorum analizinde hata oluştu: {e}")
    return data

# JSON dosyasına sonucu yazma
def save_to_json(data, file_name):
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"{file_name} dosyasına yazıldı.")


# JSON dosyasını yükleme
def load_sentiment_data(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

# Yorum yüzdelerini hesaplama ve grafiği çizme
def plot_sentiment_distribution(data):
    positive_count = sum(1 for item in data if item.get("sentiment") == "POSITIVE")
    negative_count = sum(1 for item in data if item.get("sentiment") == "NEGATIVE")
    
    total = positive_count + negative_count
    
    positive_percentage = (positive_count / total) * 100
    negative_percentage = (negative_count / total) * 100
    
    # Pasta grafiği için veriler
    labels = ['Positive', 'Negative']
    sizes = [positive_percentage, negative_percentage]
    colors = ['#66b3ff', '#ff9999']  # Mavi ve kırmızı
    explode = (0.1, 0)  # Pozitif dilimi biraz dışarı çıkarır
    
    plt.figure(figsize=(8, 6))
    plt.pie(sizes, labels=labels, colors=colors, autopct='%.1f%%', startangle=140, explode=explode)
    plt.title('Sentiment Distribution')
    plt.axis('equal')  # Daireyi düzgün bir şekilde çizmek için
    plt.show()

# Ana çalışma fonksiyonu
def main():
    input_file = "comments\\comments_-0NwrcZOKhQ.json"
    
    print("📥 JSON dosyasından yorumlar yükleniyor...")
    data = load_comments_from_json(input_file)
    print(f"✅ {len(data)} yorum yüklendi.")
    
    print("🧠 Yorumlara duygu analizi uygulanıyor...")
    updated_data = analyze_sentiment(data)
    
    result_path = "comments\\sentiment.json"
    print("💾 Sonuçlar JSON dosyasına yazılıyor...")
    save_to_json(updated_data, result_path)

    input_file = "comments\sentiment.json"
    
    print("📥 Yorum verisi yükleniyor...")
    data = load_sentiment_data(input_file)
    print(f"✅ {len(data)} yorum yüklendi.")
    
    print("📊 Yorum yüzdeleri hesaplanıyor ve görselleştiriliyor...")
    plot_sentiment_distribution(data)

if __name__ == "__main__":
    main()
