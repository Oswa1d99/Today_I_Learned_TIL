import os

# 제외할 폴더 및 파일 목록
EXCLUDE_DIRS = ['.git', '.github', 'scripts']
EXCLUDE_FILES = ['README.md']

def generate_tree(directory, level=0):
    """지정된 디렉토리의 계층 구조를 마크다운 리스트 형식으로 생성하는 재귀 함수"""
    indent = "  " * level
    tree = ""

    try:
        # 이름순으로 정렬하되, 폴더가 파일보다 먼저 오도록 정렬
        items = sorted(os.listdir(directory), key=lambda x: (os.path.isfile(os.path.join(directory, x)), x))
    except FileNotFoundError:
        return ""

    for item in items:
        if item in EXCLUDE_DIRS or item in EXCLUDE_FILES or item.startswith('.'):
            continue

        path = os.path.join(directory, item)
        
        if os.path.isdir(path):
            tree += f"{indent}- 📂 **{item}**\n"
            tree += generate_tree(path, level + 1)
        elif item.endswith('.md'):
            # 공백은 하이픈으로, .md 확장자 제거
            title = os.path.splitext(item)[0].replace(" ", "-")
            link = path.replace("\\", "/")
            tree += f"{indent}- [{title}]({link})\n"
            
    return tree

def update_readme(file_path="README.md"):
    """README.md 파일을 읽고, 마커 사이의 내용을 트리 구조로 업데이트합니다."""
    
    # --- 1. 최상위 폴더 목록을 기준으로 전체 트리 내용 생성 ---
    root_dirs = [d for d in os.listdir('.') if os.path.isdir(d) and d not in EXCLUDE_DIRS]
    root_dirs.sort()

    full_tree = ""
    for root_dir in root_dirs:
        # 각 최상위 폴더를 H3 제목으로 추가
        full_tree += f"### 📂 {root_dir}\n"
        full_tree += generate_tree(root_dir)
        full_tree += "\n"

    # --- 2. README.md 파일 읽기 ---
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            readme_content = f.read()
    except FileNotFoundError:
        print(f"❌ 오류: {file_path}를 찾을 수 없습니다.")
        return

    # --- 3. 시작과 끝 마커 정의 및 위치 찾기 ---
    start_marker = "---"
    end_marker = "---"

    start_index = readme_content.find(start_marker)
    # 첫 번째 마커 이후부터 끝 마커를 탐색
    end_index = readme_content.find(end_marker, start_index + len(start_marker))

    # --- 4. 마커가 모두 존재하면, 그 사이의 내용을 교체 ---
    if start_index != -1 and end_index != -1:
        # 시작 마커 포함 앞부분 + 새로운 트리 + 끝 마커 포함 뒷부분
        new_readme = (
            readme_content[:start_index + len(start_marker)] +
            "\n" +
            full_tree +
            readme_content[end_index:]
        )
        
        # --- 5. 새로운 내용으로 파일 전체를 덮어쓰기 ---
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_readme)
        print("✅ README.md 파일이 성공적으로 업데이트되었습니다.")
    else:
        print(f"❌ 오류: {file_path}에서 시작({start_marker}) 또는 끝({end_marker}) 마커를 찾을 수 없습니다.")

if __name__ == "__main__":
    update_readme()
