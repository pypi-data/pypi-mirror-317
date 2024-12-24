import pandas as pd
import boto3
import time
import io
import json
import hashlib
from botocore.exceptions import NoCredentialsError, ClientError

class S3Manager:
    def __init__(self, aws_access_key_id, aws_secret_access_key, bucket_name, s3_path, file_name, region_name="ap-northeast-2", log_level='INFO',custom_version_id=None):
        """
        S3Manager 객체 초기화

        Parameters:
        - aws_access_key_id: str, AWS 접근 키
        - aws_secret_access_key: str, AWS 비밀 접근 키
        - aws_session_token: str, AWS 세션 토큰 (필요한 경우)
        - bucket_name: str, S3 버킷 이름
        - file_name: str, 파일 이름
        - region_name: str, AWS 리전 (기본값: ap-northeast-2)
        """
        self.bucket_name = bucket_name
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name
        )
        self.s3_path = s3_path
        self.file_name = file_name+'.txt'
        parts = s3_path.split('/')

        # 두 번째 부분을 author로, 세 번째 부분을 id로 할당
        self.author = parts[1]
        self.id = parts[2]
        self.file_content = f"[{self.author}] [{self.id}] S3Manager 초기화 시작\n"
        self.log_level = log_level
        self.custom_version_id = custom_version_id

    def print(self, file_content,log_level = 'INFO'):
        """
        S3에 파일 업로드

        Parameters:
        - file_content: str, 파일 내용

        Returns:
        - file_content str, 파일 내용
        """
        try:
            file_content = f"{time.strftime('%Y.%m.%d - %H:%M:%S')}[{log_level}] {file_content} \n"
            if self.log_level == log_level :
                self.file_content = self.file_content + file_content
                # 업로드 옵션 설정
                upload_args = {
                    'Bucket': self.bucket_name,
                    'Key': f"{self.s3_path}{self.file_name}",
                    'Body': self.file_content
                }

                # 메타데이터에 커스텀 버전 ID 추가
                if self.custom_version_id:
                    upload_args['Metadata'] = {'custom-version': self.custom_version_id}

                # S3에 업로드
                self.s3_client.put_object(**upload_args)
            print(file_content)
            return file_content
        except NoCredentialsError:
            msg = "AWS Credentials are not available."
            print(msg)
            return msg
        except ClientError as e:
            msg = f"An error occurred: {e}"
            print(msg)
            return msg

class S3UpAndDownManager:
    def __init__(self, access_key, secret_key, region_name, bucket_name):
        """
        S3 버전 관리 데이터프레임 업로드 및 다운로드 클래스 초기화

        :param access_key: AWS 액세스 키 ID
        :param secret_key: AWS 시크릿 액세스 키
        :param region_name: AWS 리전 이름
        :param bucket_name: S3 버킷 이름
        """
        self.s3_client = boto3.client(
            's3', 
            aws_access_key_id=access_key, 
            aws_secret_access_key=secret_key,
            region_name=region_name
        )
        self.s3_resource = boto3.resource(
            's3', 
            aws_access_key_id=access_key, 
            aws_secret_access_key=secret_key,
            region_name=region_name
        )
        self.bucket_name = bucket_name

    def calculate_md5(self, data):
        """
        Calculate the MD5 hash of the given data.
        
        :param data: Data to hash
        :return: MD5 hash as a hex string
        """
        hash_md5 = hashlib.md5()
        hash_md5.update(data)
        return hash_md5.hexdigest()

    def upload_dataframe(self, data, file_key, custom_version_id=None):
        """
        데이터프레임을 CSV로 변환하여 S3에 업로드하고 무결성을 검증

        :param dataframe: 업로드할 pandas DataFrame
        :param file_key: S3에서 파일의 키 (경로 포함)
        :param custom_version_id: 명시적으로 지정할 버전 ID (선택적)
        :return: S3 업로드 결과 및 버전 ID
        """
        try:
            if isinstance(data, pd.DataFrame):
                # 데이터프레임을 CSV로 변환
                buffer = io.StringIO()
                data.to_csv(buffer, index=False)
                buffer.seek(0)
                file_data = buffer.getvalue().encode('utf-8')
            elif isinstance(data, str) and data.endswith(('.csv', '.txt', '.json')):
                # 파일 경로가 제공된 경우 파일 읽기
                with open(data, 'rb') as f:
                    file_data = f.read()
            elif isinstance(data, str):
                # 문자열 처리
                file_data = data.encode('utf-8')
            elif isinstance(data, dict):
                # JSON 객체 처리
                file_data = json.dumps(data).encode('utf-8')
            else:
                file_data = data

            # 로컬 MD5 해시 계산
            local_md5 = self.calculate_md5(file_data)
            print(f"Local MD5: {local_md5}")

            # 업로드 옵션 설정
            upload_args = {
                'Bucket': self.bucket_name,
                'Key': file_key,
                'Body': file_data
            }

            # 메타데이터에 커스텀 버전 ID 추가
            if custom_version_id:
                upload_args['Metadata'] = {'custom-version': custom_version_id}

            # S3에 업로드
            response = self.s3_client.put_object(**upload_args)

            # S3 ETag 가져오기
            s3_etag = response.get('ETag', '').strip('"')
            print(f"S3 ETag: {s3_etag}")

            # ETag와 MD5 비교
            if local_md5 == s3_etag:
                print("Upload verified successfully.")

                # 플래그 파일 생성
                flag_key = file_key.rsplit('.', 1)[0] + '.flag'
                flag_content = json.dumps({
                    'result': True,
                    'message': f"Upload completed for {file_key}"
                })
                self.s3_client.put_object(
                    Bucket=self.bucket_name,
                    Key=flag_key,
                    Body=flag_content
                )

                return {
                    'success': True, 
                    'aws_version_id': response.get('VersionId'),
                    'custom_version_id': custom_version_id
                }
            else:
                print("MD5 and ETag mismatch. Upload may have issues.")

                # 실패 플래그 파일 생성
                flag_key = file_key.rsplit('.', 1)[0] + '.flag'
                flag_content = json.dumps({
                    'result': False,
                    'message': "MD5 and ETag mismatch"
                })
                self.s3_client.put_object(
                    Bucket=self.bucket_name,
                    Key=flag_key,
                    Body=flag_content
                )

                return {
                    'success': False,
                    'error': 'MD5 and ETag mismatch'
                }

        except ClientError as e:
            # 실패 플래그 파일 생성
            flag_key = file_key.rsplit('.', 1)[0] + '.flag'
            flag_content = json.dumps({
                'result': False,
                'message': str(e)
            })
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=flag_key,
                Body=flag_content
            )

            return {
                'success': False, 
                'error': str(e)
            }

        except ClientError as e:
            # 실패 플래그 파일 생성
            flag_key = file_key.rsplit('.', 1)[0] + '.flag'
            flag_content = json.dumps({
                'result': False,
                'message': str(e)
            })
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=flag_key,
                Body=flag_content
            )

            return {
                'success': False, 
                'error': str(e)
            }

    def download_flag_file(self, flag_key):
        """
        S3에서 플래그 파일을 다운로드하여 JSON 형태로 반환

        :param flag_key: 플래그 파일의 S3 키
        :return: 플래그 파일의 내용 (dict 형태)
        """
        try:
            response = self.s3_client.get_object(Bucket=self.bucket_name, Key=flag_key)
            flag_content = json.loads(response['Body'].read().decode('utf-8'))
            return flag_content
        except ClientError as e:
            print(f"Failed to download flag file {flag_key}: {e}")
            return None

    def download_dataframe(self, file_key, custom_version_id=None, retry_limit=5):
        """
        S3에서 특정 버전의 CSV 파일을 다운로드하여 데이터프레임으로 반환하고 무결성을 검증

        :param file_key: S3에서 파일의 키 (경로 포함)
        :param custom_version_id: 다운로드할 특정 커스텀 버전 ID (선택적)
        :param retry_limit: 플래그 파일 다운로드 재시도 횟수
        :return: 다운로드된 pandas DataFrame 또는 None
        """
        try:
            # 플래그 파일 다운로드 및 검증
            flag_key = file_key.rsplit('.', 1)[0] + '.flag'
            for attempt in range(retry_limit):
                flag_content = self.download_flag_file(flag_key)
                if flag_content and flag_content.get('result'):
                    print("Flag file verified successfully.")
                    break
                else:
                    print(f"Flag file verification failed. Retrying... ({attempt + 1}/{retry_limit})")
            else:
                print("Failed to verify flag file after retries.")
                return None

            # 버킷 객체 가져오기
            bucket = self.s3_resource.Bucket(self.bucket_name)

            # 파일의 모든 버전 가져오기
            versions = list(bucket.object_versions.filter(Prefix=file_key))

            # 커스텀 버전 ID로 필터링
            if custom_version_id:
                matching_versions = [
                    v for v in versions 
                    if v.head().get('Metadata', {}).get('custom-version') == custom_version_id
                ]

                if not matching_versions:
                    print(f"Custom version {custom_version_id} not found.")
                    return None

                # 가장 최근의 매칭되는 버전 선택
                target_version = matching_versions[0]
            else:
                # 커스텀 버전 ID가 없으면 최신 버전 선택
                target_version = versions[0]

            # 객체 다운로드
            obj = target_version.get()
            csv_data = obj['Body'].read()

            # S3 ETag 가져오기
            s3_etag = obj['ETag'].strip('"')
            print(f"S3 ETag: {s3_etag}")

            # 로컬 MD5 계산
            local_md5 = self.calculate_md5(csv_data)
            print(f"Downloaded file MD5: {local_md5}")

            # ETag와 MD5 비교
            if local_md5 == s3_etag:
                print("Download verified successfully.")
            else:
                print("MD5 and ETag mismatch. Download may have issues.")
                return None

            # CSV를 DataFrame으로 변환
            return pd.read_csv(io.BytesIO(csv_data), encoding='utf-8')

        except ClientError as e:
            print(f"Error during download: {e}")
            return None