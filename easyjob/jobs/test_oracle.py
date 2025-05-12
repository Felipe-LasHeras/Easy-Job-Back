
import oracledb

# Cambia esta ruta a donde tengas instalado Oracle Instant Client
oracledb.init_oracle_client(lib_dir="C:/oracle/instantclient_19_8")

conn = oracledb.connect(user="ADMIN", dsn="sumativa_high")
print("✅ Conexión exitosa")
conn.close()
