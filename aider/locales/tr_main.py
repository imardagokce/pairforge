"""Turkish messages for pairforge's own modules (main, io, utils and others).

Keep each {placeholder} identical to the English text. See aider/i18n.py.
"""

MESSAGES = {
    "\nError running pip install: {e}": "\npip kurulumu çalıştırılırken hata: {e}",
    "\nInstallation failed.\n": "\nKurulum başarısız oldu.\n",
    "\nOAuth flow interrupted.": "\nOAuth akışı kesildi.",
    "\nPlease open this URL in your browser to connect pairforge with OpenRouter:": (
        "\nPairforge'u OpenRouter ile bağlamak için bu URL'yi tarayıcınızda açın:"
    ),
    "\nStopped watching files": "\nDosya izleme durduruldu",
    "\nWaiting up to {minutes} minutes for you to finish in the browser...": (
        "\nTarayıcıda işlemi tamamlamanız için {minutes} dakika beklenecek..."
    ),
    "--openai-api-type is deprecated, use --set-env OPENAI_API_TYPE=<value>": (
        "--openai-api-type kullanımdan kaldırıldı, bunun yerine --set"
        "-env OPENAI_API_TYPE=<value> kullanın"
    ),
    "--openai-api-version is deprecated, use --set-env OPENAI_API_VERSION=<value>": (
        "--openai-api-version kullanımdan kaldırıldı, bunun yerine --"
        "set-env OPENAI_API_VERSION=<value> kullanın"
    ),
    "--openai-organization-id is deprecated, use --set-env OPENAI_ORGANIZATION=<value>": (
        "--openai-organization-id kullanımdan kaldırıldı, bunun yerin"
        "e --set-env OPENAI_ORGANIZATION=<value> kullanın"
    ),
    "Add {patterns} to .gitignore (recommended)?": (
        ".gitignore dosyasına {patterns} eklensin mi? (önerilir)"
    ),
    "Added {patterns} to .gitignore": ".gitignore dosyasına {patterns} eklendi",
    "Added {rel_fname} to the chat": "{rel_fname} sohbete eklendi",
    "Attempting to open the issue URL in your default web browser...": (
        "Sorun URL'si varsayılan web tarayıcınızda açılmaya çalışılıyor..."
    ),
    "Authentication failed: {server_error}": "Kimlik doğrulama başarısız: {server_error}",
    "Authentication with OpenRouter failed.": "OpenRouter ile kimlik doğrulama başarısız oldu.",
    "Browser window should be opened.": "Tarayıcı penceresi açılmış olmalı.",
    "Can't initialize prompt toolkit: {err}": "Prompt toolkit başlatılamadı: {err}",
    "Commit {commit_hash} {commit_message}": "Commit {commit_hash} {commit_message}",
    "Completing authentication...": "Kimlik doğrulama tamamlanıyor...",
    "Configuration error detected.": "Yapılandırma hatası algılandı.",
    "Cost estimates may be inaccurate when using streaming and caching.": (
        "Akış ve önbellekleme kullanılırken maliyet tahminleri yanlış olabilir."
    ),
    "Could not create directory for input history: {e}": (
        "Girdi geçmişi için dizin oluşturulamadı: {e}"
    ),
    "Could not find an available port between 8484 and 8584.": (
        "8484 ile 8584 arasında kullanılabilir bir bağlantı noktası bulunamadı."
    ),
    "Could not reach Ollama at {base_url}. Is `ollama serve` running?": (
        "Ollama'ya ulaşılamadı ({base_url}). `ollama serve` çalışıyor mu?"
    ),
    "Could not reach an OpenAI-compatible server at {base_url}. Is it running?": (
        "{base_url} adresinde OpenAI uyumlu bir sunucuya ulaşılamadı. Çalışıyor mu?"
    ),
    "Cur working dir: {cwd}": "Geçerli çalışma dizini: {cwd}",
    "Detected dumb terminal, disabling fancy input and pretty output.": (
        "Basit bir terminal algılandı; gelişmiş giriş ve renkli çıktı devre dışı bırakıldı."
    ),
    "Do you trust this folder? Auto permission mode only works in trusted folders.": (
        "Bu klasöre güveniyor musunuz? Otomatik izin modu yalnızca güvenilen klasörlerde çalışır."
    ),
    "Dry run enabled, skipping commit.": "Deneme çalıştırması etkin, commit atlanıyor.",
    "Empty response received from LLM. Check your provider account?": (
        "LLM'den boş yanıt alındı. Sağlayıcı hesabınızı kontrol edin mi?"
    ),
    "End your comment with AI! to request changes or AI? to ask questions": (
        "Değişiklik istemek için yorumunuzu AI! ile, soru sormak için AI? ile bitirin"
    ),
    "Enter the issue text (Ctrl+D to finish):": "Sorun metnini girin (bitirmek için Ctrl+D):",
    "Enter the issue title (optional, press Enter to skip):": (
        "Sorun başlığını girin (isteğe bağlı, atlamak için Enter'a basın):"
    ),
    "Error checking version: {e}": "Sürüm denetlenirken hata: {e}",
    "Error exchanging code for OpenRouter key: {e}": (
        "OpenRouter anahtarı için kod değişiminde hata: {e}"
    ),
    "Error exchanging code for OpenRouter key: {status} {reason}": (
        "OpenRouter anahtarı için kod değişiminde hata: {status} {reason}"
    ),
    "Error in loading imports: {e}": "Modüller yüklenirken hata: {e}",
    "Error loading aider model settings: {e}": "aider model ayarları yüklenirken hata: {e}",
    "Error loading model metadata models: {e}": "Model meta verileri yüklenirken hata: {e}",
    "Error loading required imports. Did you install aider properly?": (
        "Gerekli modüller yüklenemedi. aider'ı düzgün kurdunuz mu?"
    ),
    "Error loading {fname}: {e}": "{fname} yüklenirken hata: {e}",
    "Error reading message file: {e}": "Mesaj dosyası okunurken hata: {e}",
    "Error when trying to read {gitignore_file}: {e}": (
        "{gitignore_file} okunurken hata oluştu: {e}"
    ),
    "Error when trying to write to {gitignore_file}: {e}": (
        "{gitignore_file} dosyasına yazılırken hata oluştu: {e}"
    ),
    "Error: 'key' not found in OpenRouter response.": (
        "Hata: OpenRouter yanıtında 'key' bulunamadı."
    ),
    "Error: Request to OpenRouter timed out during code exchange.": (
        "Hata: Kod değişimi sırasında OpenRouter isteği zaman aşımına uğradı."
    ),
    "Failed to generate commit message!": "Commit mesajı üretilemedi!",
    "Failed to run notifications command: {error_msg}": (
        "Bildirim komutu çalıştırılamadı: {error_msg}"
    ),
    "Failed to run notifications command: {e}": "Bildirim komutu çalıştırılamadı: {e}",
    "Failed to start or run temporary server: {e}": (
        "Geçici sunucu başlatılamadı veya çalıştırılamadı: {e}"
    ),
    "Files are in different git repos.": "Dosyalar farklı git depolarında.",
    'For example: --lint-cmd "python: flake8 --select=E9"': (
        'Örnek: --lint-cmd "python: flake8 --select=E9"'
    ),
    "Format should be: ENV_VAR_NAME=value": "Biçim şöyle olmalı: ENV_VAR_NAME=value",
    "Format should be: alias:model-name": "Biçim şöyle olmalı: alias:model-name",
    "Format should be: provider=key": "Biçim şöyle olmalı: provider=key",
    "Git repository created in {git_root}": "{git_root} içinde git deposu oluşturuldu",
    "Git working dir: {git_root}": "Git çalışma dizini: {git_root}",
    "Install failed, try running this command manually:": (
        "Kurulum başarısız oldu, bu komutu elle çalıştırmayı deneyin:"
    ),
    "Install playwright?": "Playwright kurulsun mu?",
    "Installation complete.": "Kurulum tamamlandı.",
    "Installing:": "Kuruluyor:",
    "Invalid --api-key format: {api_setting}": "Geçersiz --api-key biçimi: {api_setting}",
    "Invalid --set-env format: {env_setting}": "Geçersiz --set-env biçimi: {env_setting}",
    "Invalid alias format: {alias_def}": "Geçersiz takma ad biçimi: {alias_def}",
    "Is your git repo corrupted?": "Git deponuz bozulmuş olabilir mi?",
    "Loaded model metadata from:": "Model meta verileri şuradan yüklendi:",
    "Loaded model settings from:": "Model ayarları şuradan yüklendi:",
    "Loaded {fname}": "{fname} yüklendi",
    "Local model {wanted} was not found. Available: {available}": (
        "Yerel model {wanted} bulunamadı. Kullanılabilir olanlar: {available}"
    ),
    "Local servers are running but have no models. Pull or load one first, for example: ollama pull qwen2.5-coder:7b": (  # noqa: E501
        "Yerel sunucular çalışıyor ama hiç model yok. Önce bir model "
        "indirin veya yükleyin, örneğin: ollama pull qwen2.5-coder:7b"
    ),
    "Login to OpenRouter or create a free account?": (
        "OpenRouter'a giriş yapılsın mı veya ücretsiz bir hesap oluşturulsun mu?"
    ),
    "Message file not found: {message_file}": "Mesaj dosyası bulunamadı: {message_file}",
    "Model setting 'remove_reasoning' is deprecated, please use 'reasoning_tag' instead.": (
        "'remove_reasoning' model ayarı kullanımdan kaldırıldı, lütfe"
        "n bunun yerine 'reasoning_tag' kullanın."
    ),
    "More info: {url}": "Daha fazla bilgi: {url}",
    "Multiline mode: Disabled. Alt-Enter inserts newline, Enter submits text": (
        "Çok satırlı mod: Kapalı. Alt-Enter yeni satır ekler, Enter metni gönderir"
    ),
    "Multiline mode: Enabled. Enter inserts newline, Alt-Enter submits text": (
        "Çok satırlı mod: Açık. Enter yeni satır ekler, Alt-Enter metni gönderir"
    ),
    "No --test-cmd provided.": "--test-cmd sağlanmadı.",
    "No LLM model was specified and no API keys were provided.": (
        "Hiçbir LLM modeli belirtilmedi ve API anahtarı sağlanmadı."
    ),
    "No git repo found, create one to track aider's changes (recommended)?": (
        "Git deposu bulunamadı. aider'ın değişikliklerini izlemek içi"
        "n bir tane oluşturulsun mu? (önerilir)"
    ),
    "No local model servers found. Start Ollama, LM Studio or a llama.cpp server, then try again.": (  # noqa: E501
        "Yerel model sunucusu bulunamadı. Ollama, LM Studio veya bir "
        "llama.cpp sunucusunu başlatıp tekrar deneyin."
    ),
    "No model settings files loaded": "Hiçbir model ayarı dosyası yüklenmedi",
    "Note: in-chat filenames are always relative to the git working dir, not the current working dir.": (  # noqa: E501
        "Not: Sohbetteki dosya adları her zaman git çalışma dizinine "
        "göredir, geçerli çalışma dizinine göre değil."
    ),
    "OSError loading {fname}: {e}": "{fname} yüklenirken OSError: {e}",
    "Ollama at {base_url} returned HTTP {status} for /api/tags.": (
        "{base_url} adresindeki Ollama, /api/tags için HTTP {status} döndürdü."
    ),
    "Ollama at {base_url} returned an unexpected response.": (
        "{base_url} adresindeki Ollama beklenmeyen bir yanıt döndürdü."
    ),
    "Open documentation URL for more info?": (
        "Daha fazla bilgi için dokümantasyon bağlantısı açılsın mı?"
    ),
    "Open documentation about edit formats?": (
        "Düzenleme biçimleri hakkında dokümantasyon açılsın mı?"
    ),
    "Open documentation url for more info?": (
        "Daha fazla bilgi için dokümantasyon bağlantısı açılsın mı?"
    ),
    "OpenRouter authentication did not complete successfully.": (
        "OpenRouter kimlik doğrulaması başarıyla tamamlanamadı."
    ),
    "OpenRouter authentication seemed successful, but the key is still missing.": (
        "OpenRouter kimlik doğrulaması başarılı görünüyor, ancak anahtar hâlâ eksik."
    ),
    "OpenRouter provides free and paid access to many LLMs.": (
        "OpenRouter, birçok LLM'e ücretsiz ve ücretli erişim sağlar."
    ),
    "OpenRouter successfully connected.": "OpenRouter bağlantısı başarıyla kuruldu.",
    "Opening release notes: {url}": "Sürüm notları açılıyor: {url}",
    "Or run aider --no-git to proceed without using git.": (
        "Ya da git kullanmadan devam etmek için aider --no-git çalıştırın."
    ),
    "Page didn't quiesce, scraping content anyway: {url}": (
        "Sayfa tam yüklenmedi, yine de içerik kazınıyor: {url}"
    ),
    "Please consider reporting this bug to help improve aider!": (
        "aider'ı geliştirmeye yardımcı olmak için bu hatayı bildirmeyi düşünün!"
    ),
    "Please ensure a port in this range is free, or configure manually.": (
        "Lütfen bu aralıktaki bir bağlantı noktasının boş olduğundan "
        "emin olun veya elle yapılandırın."
    ),
    "Please replace 'yes:' with 'yes-always:' in this file.": (
        "Lütfen bu dosyada 'yes:' yerine 'yes-always:' yazın."
    ),
    "Processing your request...": "İsteğiniz işleniyor...",
    "Provide either a single directory of a git repo, or a list of one or more files.": (
        "Ya bir git deposunun tek bir dizinini ya da bir veya daha fazla dosya listesini verin."
    ),
    "Response: {text}": "Yanıt: {text}",
    "Run pip install?": "pip install çalıştırılsın mı?",
    "Run this command to update:": "Güncellemek için bu komutu çalıştırın:",
    "Searched for model settings files:": "Model ayarı dosyaları şu konumlarda arandı:",
    "Set OPENROUTER_API_KEY environment variable for this session only.": (
        "Yalnızca bu oturum için OPENROUTER_API_KEY ortam değişkenini ayarlayın."
    ),
    "Successfully obtained key, but failed to save it to file: {e}": (
        "Anahtar alındı ancak dosyaya kaydedilemedi: {e}"
    ),
    "Temporary authentication server failed to start in time.": (
        "Geçici kimlik doğrulama sunucusu zamanında başlatılamadı."
    ),
    "Terminal does not support pretty output (UnicodeDecodeError)": (
        "Terminal renkli çıktıyı desteklemiyor (UnicodeDecodeError)"
    ),
    "The API key was rejected by {url} (HTTP {status}).": (
        "API anahtarı {url} tarafından reddedildi (HTTP {status})."
    ),
    'The arg should be "language: cmd --args ..."': (
        'Argüman "language: cmd --args ..." biçiminde olmalıdır'
    ),
    "The file {config_file} contains a line starting with 'yes:'": (
        "{config_file} dosyasında 'yes:' ile başlayan bir satır var."
    ),
    "The git repo does not seem to have a working tree?": (
        "Git deposunda çalışma ağacı yok gibi görünüyor?"
    ),
    "The specified model '{model}' requires an OpenRouter API key, which was not found.": (
        "'{model}' modeli bir OpenRouter API anahtarı gerektiriyor, ancak anahtar bulunamadı."
    ),
    "Try running with appropriate permissions or manually add these patterns to .gitignore:": (
        "Uygun izinlerle çalıştırmayı deneyin veya bu desenleri elle .gitignore dosyasına ekleyin:"
    ),
    "Unable to add {fname}: {err}": "{fname} eklenemedi: {err}",
    "Unable to commit: {err}": "Commit yapılamadı: {err}",
    "Unable to create git repo in {git_root}": "{git_root} içinde git deposu oluşturulamadı",
    "Unable to diff: {err}": "Fark (diff) alınamadı: {err}",
    "Unable to execute lint command: {err}": "Lint komutu çalıştırılamadı: {err}",
    "Unable to lint {fname} due to RecursionError": (
        "{fname} dosyası RecursionError nedeniyle lint edilemedi"
    ),
    "Unable to list files in git repo: {err}": "Git deposundaki dosyalar listelenemedi: {err}",
    "Unable to load parser: {err}": "Ayrıştırıcı yüklenemedi: {err}",
    'Unable to parse --lint-cmd "{lint_cmd}"': '--lint-cmd "{lint_cmd}" ayrıştırılamadı',
    "Unable to proceed without an OpenRouter API key for model '{model}'.": (
        "'{model}' modeli için OpenRouter API anahtarı olmadan devam edilemiyor."
    ),
    "Unable to read git repository, it may be corrupt?": (
        "Git deposu okunamadı, bozulmuş olabilir mi?"
    ),
    "Unable to read staged files: {err}": "Hazırlanmış (staged) dosyalar okunamadı: {err}",
    "Unable to read {fname}: {err}": "{fname} okunamadı: {err}",
    "Unable to write file {filename} after {max_retries} attempts: {err}": (
        "{max_retries} denemeden sonra {filename} dosyasına yazılamadı: {err}"
    ),
    "Unable to write file {filename}: {err}": "{filename} dosyasına yazılamadı: {err}",
    "Unable to write to input history file: {err}": "Girdi geçmişi dosyasına yazılamadı: {err}",
    "Unable to write to llm history file {llm_history_file}: {err}": (
        "LLM geçmiş dosyası ({llm_history_file}) yazılamadı: {err}"
    ),
    "Unexpected error during code exchange: {e}": "Kod değişiminde beklenmeyen hata: {e}",
    'Update git email with: git config user.email "you@example.com"': (
        'Git e-postasını şununla güncelleyin: git config user.email "you@example.com"'
    ),
    'Update git name with: git config user.name "Your Name"': (
        'Git adını şununla güncelleyin: git config user.name "Your Name"'
    ),
    "Use --encoding to set the unicode encoding.": (
        "Unicode kodlamasını ayarlamak için --encoding kullanın."
    ),
    "Use --no-check-model-accepts-settings to force the '{setting}' setting.": (
        "'{setting}' ayarını zorlamak için --no-check-model-accepts-settings kullanın."
    ),
    "Use Control-C to interrupt.": "Kesmek için Control-C tuşlarına basın.",
    "Using local model {model} from {name} at {base_url}": (
        "{name} üzerinden {base_url} adresindeki {model} yerel modeli kullanılıyor"
    ),
    "Using the whole edit format, which small models handle most reliably.": (
        "Küçük modellerin en güvenilir işlediği tam düzenleme biçimi kullanılıyor."
    ),
    "Using {model} model with API key from environment.": (
        "Ortamdaki API anahtarıyla {model} modeli kullanılıyor."
    ),
    "Warning: Streaming is not supported by {model}. Disabling streaming.": (
        "Uyarı: {model} akışı (streaming) desteklemiyor. Akış devre dışı bırakılıyor."
    ),
    "Warning: Unable to write to chat history file {chat_history_file}.": (
        "Uyarı: Sohbet geçmişi dosyasına yazılamadı: {chat_history_file}."
    ),
    "Warning: {model} does not support '{setting}', ignoring.": (
        "Uyarı: {model} '{setting}' desteklemiyor, yok sayılıyor."
    ),
    "Watching source files in {directory}...": "{directory} içindeki kaynak dosyaları izleniyor...",
    "Would you like to see what's new in this version?": (
        "Bu sürümdeki yenilikleri görmek ister misiniz?"
    ),
    "You can also use this URL to file the GitHub Issue:": (
        "Bu URL'yi kullanarak GitHub Issue da açabilirsiniz:"
    ),
    "You can skip this check with --no-gitignore": (
        "Bu kontrolü --no-gitignore ile atlayabilirsiniz"
    ),
    "You can skip this check with --no-show-model-warnings": (
        "Bu kontrolü --no-show-model-warnings ile atlayabilirsiniz"
    ),
    "You may be able to convert your repo: git update-index --index-version=2": (
        "Deponuzu dönüştürebilirsiniz: git update-index --index-version=2"
    ),
    "You should probably run aider in your project's directory, not your home dir.": (
        "aider'ı ana dizininizde değil, proje dizininizde çalıştırmanız önerilir."
    ),
    "pairforge only works with git repos with version number 1 or 2.": (
        "pairforge yalnızca 1 veya 2 sürüm numaralı git depolarıyla çalışır."
    ),
    "pairforge will load the OpenRouter key automatically in future sessions.": (
        "pairforge, OpenRouter anahtarını sonraki oturumlarda otomatik olarak yükleyecek."
    ),
    "{filename}: file not found error": "{filename}: dosya bulunamadı",
    "{filename}: is a directory": "{filename}: bir dizin",
    "{filename}: unable to read: {err}": "{filename}: okunamadı: {err}",
    "{filename}: {e}": "{filename}: {e}",
    "{fname} is a directory, but --no-git selected.": "{fname} bir dizin, ancak --no-git seçildi.",
    "{fname} is a directory, not provided alone.": "{fname} bir dizin; tek başına verilmedi.",
}
