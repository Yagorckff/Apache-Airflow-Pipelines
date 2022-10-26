# Vamos desenvolver o nosso primeiro workflow
# É necessário colocar este arquivo dentro da pasta de DAGS do AIRFLOW


# Verificar no arquivo de configuração do AIRFLOW o path dos DAGS
# dags_folder = /root/airflow/dags

# Módulos do Airflow
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator


# Vamos criar um objeto DAG
# Para isso, devemos especificar alguns parâmetros básicos, tais como:
# Quando se tornará ativo
# Quais os intervalos que queremos que execute
# Quantas tentativas devem ser feitas caso alguma de suas tarefas falhe
# Vamos definir esses parâmetros

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    # Exemplo: Inicia em 20 de Janeiro de 2021
    'start_date': datetime(2024, 10, 24),
    'email': ['yago.devb@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    # Em caso de erros, tente rodar novamente apenas 1 vez
    'retries': 1,
    # Tente novamente após 30 segundos depois do erro
    'retry_delay': timedelta(seconds=30),
    # Execute uma vez a cada 15 minutos
    'schedule_interval': '*/15 * * * *'
}



# Exemplo de definição de schedule
# .---------------- minuto (0 - 59)
# |  .------------- hora (0 - 23)
# |  |  .---------- dia do mês (1 - 31)
# |  |  |  .------- mês (1 - 12)
# |  |  |  |  .---- dia da semana (0 - 6) (Domingo=0 or 7)
# |  |  |  |  |
# *  *  *  *  * (nome do usuário que vai executar o comando)



# Definimos nossos parâmetros.
# Vamos agora informar ao nosso DAG o que ele deve fazer.
# Fazemos isso declarando tarefas diferentes - T1 e T2.
# Devemos também definir qual tarefa depende da outra.

with DAG(
    dag_id='minha_primeira_dag',
    default_args=default_args, #de onde vai pegar o conjunto de chaves e valores
    schedule_interval=None,
    tags=['exemplo1'], #tags, usadas para organizar melhor as tarefas, podendo ser usadas para fazer filtros de pesquisa na página de dags
) as dag:

    # Vamos Definir a nossa Primeira Tarefa
    t1 = BashOperator(bash_command="touch ~/meu_arquivo_01.txt", task_id="criar_arquivo")
    #esse processo cria um arquivo, task_id é o nome da task.
    # Vamos definir a nossa segunda task
    t2 = BashOperator(bash_command="mv ~/meu_arquivo_01.txt ~/meu_arquivo_01_MUDOU.txt", task_id="mudar_nome_do_arquivo")
    #nesse processo muda o nome do arquivo
    # Configurar a tarefa T2 para ser dependente da tarefa T1
    t1 >> t2 #aqui escolhemos a ordem de execução das tarefas.
