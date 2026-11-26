#!/usr/bin/env python3
import asyncio
import base64
import hashlib
import json
import math
import os
import re
import shutil
import struct
import subprocess
import sys
import time
import wave
from datetime import datetime

JOB_TITLE = "khalid_bin_yazid_ep5_style_auto"
FPS = 24
WIDTH = 1080
HEIGHT = 1920
JPEG_QUALITY = 72
VOICE_NAME = "id-ID-ArdiNeural"
VOICE_RATE = "-3%"
VOICE_PITCH = "-1Hz"

SEGMENTS = [
    {
        "id": "scene1",
        "text": "Malam itu juga, setelah pejabat istana pergi, Khalid tidak tidur. Dia tidak kembali ke kamar. Dia kembali ke lab yang masih bau asap itu."
    },
    {
        "id": "scene2",
        "text": "Stephanus mengira Khalid akan istirahat. Ternyata Khalid memanggil tiga penyalin. Tiga orang yang tangannya paling cepat, matanya paling teliti. Dia meletakkan catatan yang selamat dari api kemarin di tengah meja, dan dia bilang pelan, \"Salin. Salin semuanya, malam ini juga.\""
    },
    {
        "id": "scene3",
        "text": "Kamu bisa bayangkan, kan? Di ruangan yang masih hitam bekas ledakan, ada bunyi pena yang tidak berhenti. Srek, srek, srek. Bau tinta bercampur bau asap. Tangan mereka pegal, mata mereka perih, tapi tidak ada yang berhenti. Karena Khalid sudah bilang, \"Kalau ilmu ini hanya ada di satu tempat, besok bisa dibakar lagi. Kalau ilmu ini ada di banyak tempat, tidak ada yang bisa membunuhnya.\""
    },
    {
        "id": "scene4",
        "text": "Pagi harinya, saat matahari baru naik di Damaskus, tiga karavan sudah siap. Satu ke Alexandria, ke tempat Stephanus berasal. Satu ke Kufah, kota yang nanti akan jadi kota ilmu. Satu ke Mekkah. Setiap karavan membawa salinan yang sama. Bukan emas. Bukan hadiah. Tapi gulungan yang isinya: api harus dikendalikan, ilmu adalah apa yang bisa diulang."
    },
    {
        "id": "scene5",
        "text": "Orang-orang di pasar mengira karavan itu membawa barang dagangan. Mereka tidak tahu, yang dibawa itu adalah masa depan. 50 tahun kemudian, seorang anak muda di Kufah bernama Jabir ibn Hayyan akan menemukan salah satu salinan itu. Dan dari salinan itu, dia akan membangun kimia modern."
    },
    {
        "id": "scene6",
        "text": "Tapi besok, di Episode 6, ada yang lebih berat. Karena setelah karavan itu pergi, Khalid sendirian. Badannya mulai lemah. Dia sudah menghabiskan hartanya untuk buku dan penyalin. Dan dia mulai sadar, waktunya tidak banyak lagi. Apa yang akan dia tulis di catatan terakhirnya sebelum dia pergi? Follow, biar besok kamu tidak ketinggalan warisannya. Simpan video ini, karena cara Khalid menyebarkan ilmu ini adalah cara yang masih kita pakai sampai hari ini."
    }
]

FILES_B64 = {
    "package.json": "ewogICJuYW1lIjogImtoYWxpZC1iaW4teWF6aWQtZXA1LXN0eWxlLWF1dG8iLAogICJ2ZXJzaW9uIjogIjEuMC4wIiwKICAicHJpdmF0ZSI6IHRydWUsCiAgImRlcGVuZGVuY2llcyI6IHsKICAgICJyZW1vdGlvbiI6ICI0LjAuMjIwIiwKICAgICJAcmVtb3Rpb24vY2xpIjogIjQuMC4yMjAiLAogICAgInJlYWN0IjogIjE4LjMuMSIsCiAgICAicmVhY3QtZG9tIjogIjE4LjMuMSIsCiAgICAibHVjaWRlLXJlYWN0IjogIjAuNDYwLjAiLAogICAgInpvZCI6ICIzLjIzLjgiCiAgfSwKICAiZGV2RGVwZW5kZW5jaWVzIjogewogICAgIkB0eXBlcy9yZWFjdCI6ICIxOC4zLjEyIiwKICAgICJ0eXBlc2NyaXB0IjogIjUuNi4zIgogIH0KfQ==",
    "tsconfig.json": "ewogICJjb21waWxlck9wdGlvbnMiOiB7CiAgICAidGFyZ2V0IjogIkVTMjAyMiIsCiAgICAibW9kdWxlIjogIkNvbW1vbkpTIiwKICAgICJqc3giOiAicmVhY3QtanN4IiwKICAgICJzdHJpY3QiOiB0cnVlLAogICAgImVzTW9kdWxlSW50ZXJvcCI6IHRydWUsCiAgICAic2tpcExpYkNoZWNrIjogdHJ1ZSwKICAgICJyZXNvbHZlSnNvbk1vZHVsZSI6IHRydWUsCiAgICAibW9kdWxlUmVzb2x1dGlvbiI6ICJub2RlIiwKICAgICJmb3JjZUNvbnNpc3RlbnRDYXNpbmdJbkZpbGVOYW1lcyI6IHRydWUKICB9LAogICJpbmNsdWRlIjogWwogICAgInNyYy8qKi8qIgogIF0KfQ==",
    "remotion.config.ts": "aW1wb3J0IHsgQ29uZmlnIH0gZnJvbSAnQHJlbW90aW9uL2NsaS9jb25maWcnOwoKQ29uZmlnLnNldFZpZGVvSW1hZ2VGb3JtYXQoJ2pwZWcnKTsKQ29uZmlnLnNldEpwZWdRdWFsaXR5KDcyKTsK",
    "src/index.ts": "aW1wb3J0IHsgcmVnaXN0ZXJSb290IH0gZnJvbSAncmVtb3Rpb24nOwppbXBvcnQgeyBSZW1vdGlvblJvb3QgfSBmcm9tICcuL1Jvb3QnOwoKcmVnaXN0ZXJSb290KFJlbW90aW9uUm9vdCk7Cg==",
    "src/Root.tsx": "aW1wb3J0IFJlYWN0IGZyb20gJ3JlYWN0JzsKaW1wb3J0IHsgQ29tcG9zaXRpb24gfSBmcm9tICdyZW1vdGlvbic7CmltcG9ydCBtYW5pZmVzdCBmcm9tICcuLi9wdWJsaWMvbWFuaWZlc3QuanNvbic7CmltcG9ydCB7IE1haW5WaWRlbyB9IGZyb20gJy4vVmlkZW8nOwoKZXhwb3J0IGNvbnN0IFJlbW90aW9uUm9vdDogUmVhY3QuRkMgPSAoKSA9PiB7CiAgcmV0dXJuICgKICAgIDxDb21wb3NpdGlvbgogICAgICBpZD0iTWFpbkNvbXAiCiAgICAgIGNvbXBvbmVudD17TWFpblZpZGVvfQogICAgICBkdXJhdGlvbkluRnJhbWVzPXttYW5pZmVzdC50b3RhbEZyYW1lcyB8fCAyMjgwfQogICAgICBmcHM9e21hbmlmZXN0LmZwcyB8fCAyNH0KICAgICAgd2lkdGg9ezEwODB9CiAgICAgIGhlaWdodD17MTkyMH0KICAgIC8+CiAgKTsKfTsK",
    "src/styles/themes.ts": "aW1wb3J0IHsgU3VidGl0bGVTdHlsZUNvZGUgfSBmcm9tICcuLi9jb21wb25lbnRzL1N1YnRpdGxlRW5naW5lJzsKaW1wb3J0IHsgVHJhbnNpdGlvblZhcmlhbnQgfSBmcm9tICcuLi9tb3Rpb24vU2NlbmVDb250YWluZXInOwoKZXhwb3J0IHR5cGUgQXV0b1N0eWxlUGFja0NvZGUgPQogIHwgJ2NpbmVtYXRpYy1nb2xkJwogIHwgJ2FyY2hpdmUtY29sbGFnZScKICB8ICd3aGl0ZWJvYXJkJwogIHwgJ2lzb21ldHJpYycKICB8ICdibHVlcHJpbnQnCiAgfCAna2luZXRpYyc7CgpleHBvcnQgdHlwZSBBbmltYXRpb25Db2RlID0gJ0FOTS1TTkFQUFknIHwgJ0FOTS1TTU9PVEgnIHwgJ0FOTS1LSU5FVElDJyB8ICdBTk0tRkxPQVQnIHwgJ0FOTS1HUklEJzsKZXhwb3J0IHR5cGUgRm9udENvZGUgPSAnRk5ULU1PREVSTicgfCAnRk5ULUlNUEFDVCcgfCAnRk5ULUVESVQnIHwgJ0ZOVC1URUNIJyB8ICdGTlQtUk9VTkQnOwpleHBvcnQgdHlwZSBWb0NvZGUgPSAnVk8tRU5FUkdFVElDJyB8ICdWTy1TVE9SWScgfCAnVk8tTkVXUyc7CmV4cG9ydCB0eXBlIFNmeFByb2ZpbGVDb2RlID0gJ1NGWC1TTkFQUFknIHwgJ1NGWC1TVUJUTEUnIHwgJ1NGWC1URUNIJyB8ICdTRlgtT0ZGJzsKZXhwb3J0IHR5cGUgQmdtTW9vZENvZGUgPSAnd2FybS1wYWQnIHwgJ3RlY2gtcHVsc2UnIHwgJ3VwYmVhdC1wbHVjaycgfCAnb2ZmJzsKCmV4cG9ydCBpbnRlcmZhY2UgU2NlbmVTdHlsZVRoZW1lIHsKICBjb2RlOiBBdXRvU3R5bGVQYWNrQ29kZTsKICBsYWJlbDogc3RyaW5nOwogIGlzRGFyazogYm9vbGVhbjsKICBiZ1ByaW1hcnk6IHN0cmluZzsKICBiZ1NlY29uZGFyeTogc3RyaW5nOwogIGNhcmRCZzogc3RyaW5nOwogIGNhcmRCb3JkZXI6IHN0cmluZzsKICB0cmFja0JnOiBzdHJpbmc7CiAgdGV4dFByaW1hcnk6IHN0cmluZzsKICB0ZXh0TXV0ZWQ6IHN0cmluZzsKICBhY2NlbnQ6IHN0cmluZzsKICBhY2NlbnRUZXh0OiBzdHJpbmc7CiAgc3VidGl0bGU6IFN1YnRpdGxlU3R5bGVDb2RlOwogIGZvbnQ6IEZvbnRDb2RlOwogIGFuaW1hdGlvbjogQW5pbWF0
