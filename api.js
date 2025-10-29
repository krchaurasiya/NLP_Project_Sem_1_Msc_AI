import axios from "axios";
const API = axios.create({ baseURL: "http://localhost:5000" });

export async function uploadFile(file, src_lang='pt', target_langs='en,hi') {
  const form = new FormData();
  form.append('file', file);
  form.append('src_lang', src_lang);
  form.append('target_langs', target_langs);
  form.append('ocr_mode', 'auto');
  const res = await API.post('/translate', form, {
    headers: { 'Content-Type': 'multipart/form-data' }
  });
  return res.data;
}


