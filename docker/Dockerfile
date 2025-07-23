FROM openjdk:21

WORKDIR /app

# Audiveris jar’ı kopyala
COPY audiveris.jar /audiveris/audiveris.jar

# run scriptini ekle ve izin ver
COPY run_audiveris.sh /app/run_audiveris.sh
RUN chmod +x /app/run_audiveris.sh

# Giriş/çıkış klasörleri
RUN mkdir -p /input /output

CMD ["/app/run_audiveris.sh"]
