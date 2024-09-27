import asyncio
import dc_api
from datetime import datetime

# async def search_artist_board(api, artist_name):
#     """아티스트 이름으로 해당 게시판 검색."""
#     async for board in api.search_boards(artist_name):
#         if artist_name.lower() in board.name.lower():
#             return board.board_id
#     return None

async def fetch_posts_in_time_range(api, board_id, start_date, end_date):
    """특정 기간 내의 게시글을 가져오는 함수."""
    post_count = 0
    total_views = 0
    total_votes = 0
    total_comments = 0

    async for index in api.board(board_id=board_id):
        doc = await index.document()

        # 게시물 날짜가 기간 내에 있는지 확인
        post_date = doc.time
        if start_date <= post_date <= end_date:
            post_count += 1
            total_views += doc.view_count
            total_votes += doc.voteup_count

            # 댓글 수를 합산
            total_comments += doc.comment_count

            # 게시물과 댓글 정보 출력
            print(f"제목: {doc.title}, 조회수: {doc.view_count}, 추천수: {doc.voteup_count}, 댓글수: {doc.comment_count}")

    return post_count, total_views, total_votes, total_comments

async def run(board_id, start_date, end_date):
    async with dc_api.API() as api:
        # 아티스트 게시판 검색
        # board_id = await search_artist_board(api, artist_name)
        # if not board_id:
        #     print(f"'{artist_name}'로 검색된 게시판이 없습니다.")
        #     return

        # 특정 기간 내 게시글 크롤링
        post_count, total_views, total_votes, total_comments = await fetch_posts_in_time_range(
            api, board_id, start_date, end_date)

        # 최종 통계 출력 및 저장
        print(f"기간 내 게시물 수: {post_count}")
        print(f"총 조회수: {total_views}")
        print(f"총 추천수: {total_votes}")
        print(f"총 댓글 수: {total_comments}")

        # 결과를 파일로 저장
        with open(f"{board_id}_stats_{start_date}_{end_date}.txt", "w") as f:
            f.write(f"기간 내 게시물 수: {post_count}\n")
            f.write(f"총 조회수: {total_views}\n")
            f.write(f"총 추천수: {total_votes}\n")
            f.write(f"총 댓글 수: {total_comments}\n")

# 실행할 때 아티스트 이름과 기간을 설정하여 호출
board_id = "programming"
start_date = datetime(2023, 1, 1)
end_date = datetime(2023, 12, 31)

asyncio.run(run(board_id, start_date, end_date))
