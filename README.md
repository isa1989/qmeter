
PROYEKTİN KONFİQRASİYA EDİLMƏSİ VƏ DATABAZANIN KÖÇÜRÜLMƏSİ
1.Ilkin olaraq docker containerini up build edirik 
  docker-compose up --build -d

2.Container qalxdiqdan sonra aşağıdakı konamda ilə konteynerə daxil oluruq və göndırilən https://qmeter-fb-dev.s3.amazonaws.com/media/feedback.json url-dəki dataları restore edirik
  docker exec -it qmeter_web bash 

3.Bunun üçün komanda yazmişam bu komandanı run edirik. 
  python manage.py qmeterdata_restore

TAPŞIRIĞIN HƏLLİ

1.aggregation.py adında yaradılmış pyton faylında MongoAggregation sinifi yaradırıq.
2.MongoDB connection qururuq ve bizə lazım olan db ve collectionu qeyd edirik
  self.db_name = os.getenv("DATABASE_NAME")
  self.collection_name = "feed_collection"
  self.mongo_host = os.getenv("DATABASE_HOST")
  self.mongo_port = os.getenv("DATABASE_PORT", 27017)  # Varsayılan port
  self.client = MongoClient(
            f"mongodb://{self.mongo_host}:{self.mongo_port}/{self.db_name}"
        )
  self.db = self.client[self.db_name]
  self.collection = self.db[self.collection_name]
3.MongoDB-də aggregate əməliyyatı üçün  pipeline və aşağıdakıları edir:
  $unwind: feedback_rate adlı array-ləri açır (yəni hər bir feedback üçün ayrıca sənəd yaradır).
  $group: Eyni filial və xidmət adı ilə olan məlumatları qruplaşdırır, hər bir qiymətləndirmə üçün (rating 1-dən 5-ə qədər) sayı hesablayır.
  $addFields: Ümumi qiymətləndirmə sayını (total_count) və ağırlıqlı cəmi (weighted_sum) əlavə edir.
  $addFields: Hər bir xidmətin ümumi qiymətləndirmə balını (score) hesablamaq üçün total_count və weighted_sum dəyərlərini istifadə edir.
  $group: Hər bir filial üçün bütün xidmətləri bir araya gətirir.
  $project: Nəticəni düzəldir və yalnız lazım olan sahələri göstərir.
4.http://127.0.0.1:8000/feedback-rate/
  localda gostərirəm çünki tapşırıqda domain verilməyib (deploy elemek üçün) test üçün.
5. tapşırıqdan elave burada Pythonic Solution adında field yaratmışam ve elave olaraq yazdığım viewsda pyhonic olaraq verilen tapşırığı hell edirem ve mongodb ile yazılmlş query ile yan yana yaziram.
   ve burada mongo ve pythonic helleri müqayisə edə bilərik(her ikisinde data eyni olmalidir ve eynidir!)
   
