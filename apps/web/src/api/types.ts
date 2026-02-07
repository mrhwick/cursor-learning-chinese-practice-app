export type UserPublic = { id: number; email: string; role: "teacher" | "student" };

export type PhrasePublic = {
  id: number;
  classroom_id: number;
  chinese: string;
  pinyin: string;
  english: string;
  notes: string | null;
  created_at: string;
  has_model_audio: boolean;
};

export type ClassroomPublic = {
  id: number;
  name: string;
  invite_code: string;
  owner_id: number;
  created_at: string;
};

export type FeedbackPublic = {
  id: number;
  submission_id: number;
  author_id: number;
  comment: string;
  score_tones: number;
  score_clarity: number;
  created_at: string;
};

