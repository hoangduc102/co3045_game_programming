# Zombie Head Smash Game 🧟‍♂️💥

## Giới thiệu
Zombie Head Smash là một trò chơi arcade hành động được phát triển bằng Python và Pygame. Người chơi cần tiêu diệt các đầu zombie xuất hiện ngẫu nhiên trên màn hình trong thời gian giới hạn để đạt điểm số cao nhất.

## Tính năng nổi bật ✨

### 🎮 Chế độ chơi đa dạng
- **Classic**: Zombie không tự động biến mất, thời gian chơi 120 giây
- **Easy**: Zombie sống lâu hơn, thời gian chơi 75 giây
- **Medium**: Độ khó trung bình, thời gian chơi 60 giây  
- **Hard**: Zombie biến mất nhanh, thời gian chơi 45 giây

### 🌈 Hiệu ứng visual đặc sắc
- **Hệ thống Combo**: Điểm số tăng theo combo, hiệu ứng thay đổi theo mức combo
- **Particle Effects**: Hiệu ứng máu, bụi, sao khi tiêu diệt zombie
- **Screen Shake**: Rung màn hình khi đạt combo cao
- **Mouse Trail**: Vệt chuột màu sắc theo chuyển động
- **Floating Text**: Văn bản bay lên hiển thị điểm số
- **Rainbow Effects**: Hiệu ứng cầu vồng cho combo cao

### 🎵 Âm thanh sống động
- Nhạc nền trong game và menu
- Âm thanh khi nhấp chuột
- Âm thanh khi tiêu diệt zombie

### 🏆 Hệ thống điểm số
- Điểm cơ bản: +1 điểm mỗi zombie tiêu diệt
- Hệ thống combo: Điểm nhân với số combo liên tiếp
- Penalty: -1 điểm mỗi lần bỏ lỡ hoặc zombie tự biến mất
- Tracking combo cao nhất đạt được

## Cài đặt và chạy game 🚀

### Yêu cầu hệ thống
- Python 3.7 trở lên
- Pygame library
- Windows/macOS/Linux

### Cách cài đặt

1. **Clone hoặc download project**
```bash
git clone [repository-url]
cd zombie_game
```

2. **Cài đặt Pygame**
```bash
pip install pygame
```

3. **Chạy game**

**Cách 1: Sử dụng Python**
```bash
python main.py
```

**Cách 2: Sử dụng file batch (Windows)**
```bash
run_game.bat
```

## Cấu trúc thư mục 📁

```
zombie_game/
├── main.py                     # File chính khởi chạy game
├── game.py                     # Logic game chính
├── zombie.py                   # Class và logic zombie
├── ui.py                       # Giao diện người dùng
├── effects.py                  # Hiệu ứng visual và particle
├── constants.py                # Hằng số và cấu hình game
├── utils.py                    # Tiện ích hỗ trợ
├── images/                     # Thư mục hình ảnh
│   ├── background.png          # Hình nền game
│   ├── button_hover.png        # Hình button khi hover
│   ├── button_normal.png       # Hình button bình thường
│   ├── menu_background.png     # Hình nền menu
│   ├── splat.png               # Hiệu ứng máu
│   └── zombie_head.png         # Hình đầu zombie
├── sounds/                     # Thư mục âm thanh
│   ├── background_music.mp3    # Nhạc nền
│   ├── click_sound.wav         # Âm thanh click
│   └── splat_sound.wav         # Âm thanh tiêu diệt zombie
├── run_game.bat                # Script chạy game (Windows)
└── README.md                   # Hướng dẫn chi tiết game
```

## Cách chơi 🎯

### Điều khiển
- **Chuột trái**: Click để tiêu diệt zombie
- **Di chuyển chuột**: Tạo hiệu ứng trail

### Luật chơi
1. Zombie xuất hiện ngẫu nhiên tại 9 vị trí cố định
2. Click vào zombie để tiêu diệt và ghi điểm
3. Zombie sẽ tự biến mất sau một thời gian (trừ chế độ Classic)
4. Tạo combo bằng cách tiêu diệt zombie liên tiếp
5. Tránh click nhầm (miss) để giữ combo
6. Cố gắng đạt điểm cao nhất trong thời gian cho phép

### Hệ thống Combo
- **1-4 combo**: Hiệu ứng bình thường, +điểm theo combo
- **5-9 combo**: Hiệu ứng "GREAT", màu sắc đặc biệt, hiệu ứng sóng
- **10+ combo**: Hiệu ứng "EPIC", văn bản cầu vồng, hiệu ứng nổ và sao

## Chi tiết kỹ thuật 💻

### Classes chính
- **Game**: Class quản lý toàn bộ game logic
- **Zombie**: Class đối tượng zombie với animation
- **Button**: Class cho các nút bấm UI  
- **Particle**: Class hiệu ứng hạt
- **FloatingText**: Class văn bản bay
- **ScreenShake**: Class hiệu ứng rung màn hình
- **ExplosionEffect**: Class hiệu ứng nổ
- **StarEffect**: Class hiệu ứng sao
- **WaveEffect**: Class hiệu ứng sóng

### Tính năng nâng cao
- Hệ thống particle effects với physics
- Animation mượt mà cho zombie pop-up
- Hiệu ứng cảnh báo khi zombie sắp biến mất
- Mouse trail với hiệu ứng rainbow
- Glow effects cho UI elements
- Responsive button system

## Customization 🛠️

### Thay đổi độ khó
Có thể điều chỉnh các thông số trong hàm `start_game()`:
- `game_duration`: Thời gian chơi (ms)
- `zombie_speed_multiplier`: Tốc độ biến mất của zombie
- `max_zombies_on_screen`: Số zombie tối đa cùng lúc
- `spawn_interval_min/max`: Khoảng thời gian spawn zombie

### Thay đổi vị trí spawn
Chỉnh sửa mảng `ZOMBIE_SPAWN_POINTS` để thay đổi vị trí xuất hiện zombie.

### Thay đổi màu sắc
Các màu được định nghĩa ở đầu file, có thể tùy chỉnh:
- `SCORE_COLORS`: Màu điểm số theo combo
- `RAINBOW_COLORS`: Màu cầu vồng cho hiệu ứng

## Phát triển thêm 🔮

### Ý tưởng mở rộng
- [ ] Thêm power-ups (đóng băng thời gian, điểm nhân đôi)
- [ ] Zombie đặc biệt (nhanh hơn, chậm hơn, bonus points)
- [ ] Hệ thống achievement/thành tích
- [ ] Leaderboard local
- [ ] Thêm level/stage system
- [ ] Boss zombies
- [ ] Multiplayer mode

### Cải thiện hiệu năng
- Tối ưu particle system
- Preload assets
- Object pooling cho zombie

## Troubleshooting 🔧

### Lỗi thường gặp

**Không có âm thanh**
- Kiểm tra file âm thanh trong thư mục `sounds/`
- Đảm bảo Pygame được cài đặt đầy đủ

**Hình ảnh không hiển thị**
- Kiểm tra file hình ảnh trong thư mục `images/`
- Đảm bảo định dạng file đúng (PNG)

**Game chạy chậm**
- Đóng các ứng dụng khác
- Giảm số lượng particle effects

## Tác giả 👨‍💻
Game được phát triển như một project học tập tại HCMUT.

## License 📄
Project này được tạo ra cho mục đích học tập và giải trí.

---

🎮 **Chúc bạn chơi game vui vẻ và đạt điểm số cao!** 🏆
