-- ============================================================
-- MoodPing DB Schema (MySQL 8.0)
-- Spring Boot 버전(moodping-backend)과 동일한 스키마
-- 문자셋: utf8mb4 (이모지 저장 지원)
-- ============================================================

-- 1. 감정 기록 테이블
CREATE TABLE IF NOT EXISTS mood_record
(
    id          BIGINT       NOT NULL AUTO_INCREMENT,
    user_id     VARCHAR(100) NULL     COMMENT '로그인 사용자 ID (없으면 NULL)',
    anon_id     VARCHAR(100) NULL     COMMENT '비로그인 사용자 익명 ID',
    record_date DATE         NOT NULL COMMENT '기록 날짜 (서버 기준)',
    recorded_at DATETIME     NOT NULL COMMENT '기록 일시 (서버 기준)',
    mood_emoji  VARCHAR(20)  NOT NULL COMMENT '감정 이모지 문자 (예: 😊)',
    intensity   TINYINT      NOT NULL COMMENT '감정 강도 0~10',
    mood_text   VARCHAR(500) NULL     COMMENT '감정 설명 텍스트 (선택)',
    created_at  DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at  DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    INDEX idx_mood_record_user_id (user_id),
    INDEX idx_mood_record_anon_id (anon_id),
    INDEX idx_mood_record_recorded_at (recorded_at),
    CONSTRAINT chk_intensity CHECK (intensity >= 0 AND intensity <= 10)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_unicode_ci;

-- 2. AI 감정 분석 결과 테이블
CREATE TABLE IF NOT EXISTS mood_analysis
(
    id            BIGINT       NOT NULL AUTO_INCREMENT,
    record_id     BIGINT       NOT NULL COMMENT 'mood_record.id FK',
    user_id       VARCHAR(100) NULL     COMMENT '분석 요청 사용자 ID',
    analysis_text TEXT         NULL     COMMENT 'LLM이 생성한 분석 문단',
    created_at    DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    INDEX idx_mood_analysis_record_id (record_id),
    CONSTRAINT fk_mood_analysis_record FOREIGN KEY (record_id) REFERENCES mood_record (id) ON DELETE CASCADE
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_unicode_ci;

-- 3. 유저 퍼널 이벤트 로그 테이블
CREATE TABLE IF NOT EXISTS event_log
(
    id          BIGINT       NOT NULL AUTO_INCREMENT,
    event_id    VARCHAR(100) NOT NULL COMMENT '프론트에서 생성한 이벤트 고유 UUID',
    session_id  VARCHAR(100) NOT NULL COMMENT '세션 고유 UUID',
    user_id     VARCHAR(100) NULL     COMMENT '로그인 사용자 ID',
    anon_id     VARCHAR(100) NULL     COMMENT '비로그인 사용자 익명 ID',
    event_name  VARCHAR(50)  NOT NULL COMMENT '이벤트 이름',
    occurred_at DATETIME     NOT NULL COMMENT '이벤트 발생 일시',
    metadata    JSON         NULL     COMMENT '이벤트 추가 데이터',
    PRIMARY KEY (id),
    UNIQUE KEY uk_event_id (event_id),
    INDEX idx_event_log_session_id (session_id),
    INDEX idx_event_log_event_name (event_name),
    INDEX idx_event_log_occurred_at (occurred_at),
    INDEX idx_event_log_user_id (user_id),
    INDEX idx_event_log_anon_id (anon_id)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_unicode_ci;
