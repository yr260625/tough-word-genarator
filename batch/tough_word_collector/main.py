import time
from batch.tough_word_collector.main_usecase import MainUsecase


if __name__ == '__main__':
    retry_counter = 0
    start_page = 1
    usecase = MainUsecase()

    try:
        for page in range(start_page, start_page + 1):
            usecase.collect_board_responses_per_page(page)
            time.sleep(5)
    except Exception as e:
        print(e)
        raise e