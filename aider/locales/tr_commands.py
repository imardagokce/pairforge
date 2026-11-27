"""Turkish messages for aider/commands.py."""

MESSAGES = {
    "\nExecuting: {cmd}": "\nÇalıştırılıyor: {cmd}",
    "\nFiles in chat:\n": "\nSohbetteki dosyalar:\n",
    "\nNo files in chat, git repo, or read-only list.": (
        "\nSohbette, git deposunda veya salt okunur listede dosya yok."
    ),
    "\nOr a valid edit format:\n": "\nYa da geçerli bir düzenleme biçimi:\n",
    "\nRead-only files:\n": "\nSalt okunur dosyalar:\n",
    "  (no models loaded)": "  (yüklü model yok)",
    "... added to chat.": "... sohbete eklendi.",
    "/drop to remove": "kaldırmak için /drop kullanın",
    (
        "Add files to the chat so aider can edit them or review them in "
        "detail"
    ): (
        "Aider'ın dosyaları düzenleyebilmesi veya ayrıntılı "
        "inceleyebilmesi için dosyaları sohbete ekleyin"
    ),
    (
        "Add files to the chat that are for reference only, or turn added "
        "files to read-only"
    ): (
        "Yalnızca başvuru için dosyaları sohbete ekleyin veya eklenen "
        "dosyaları salt okunur yapın"
    ),
    "Add {k_tokens:.1f}k tokens of command output to the chat?": (
        "Komut çıktısının {k_tokens:.1f}k token'ı sohbete eklensin mi?"
    ),
    "Added clipboard image to the chat: {abs_file_path}": (
        "Panodaki resim sohbete eklendi: {abs_file_path}"
    ),
    (
        "Added {added_files} files from directory {original_name} to "
        "read-only files."
    ): (
        "{original_name} dizininden {added_files} dosya salt okunur "
        "dosyalara eklendi."
    ),
    "Added {fname} to the chat": "{fname} sohbete eklendi",
    "Added {num_lines} {line_plural} of output to the chat.": (
        "Sohbete {num_lines} {line_plural} çıktı eklendi."
    ),
    "Added {original_name} to read-only files.": "{original_name} salt okunur dosyalara eklendi.",
    "Alias for /editor: Open an editor to write a prompt": (
        "/editor için takma ad: Bir istem yazmak için düzenleyici açın"
    ),
    (
        "Alias for `/code Ok, please go ahead and make those changes.` "
        "(any args are appended)"
    ): (
        "`/code Ok, please go ahead and make those changes.` için takma "
        "ad (verilen tüm argümanlar eklenir)"
    ),
    "All chat history cleared.": "Tüm sohbet geçmişi temizlendi.",
    "All files dropped and chat history cleared.": (
        "Tüm dosyalar bırakıldı ve sohbet geçmişi temizlendi."
    ),
    (
        "An unexpected error occurred while copying to clipboard: {error}"
    ): (
        "Panoya kopyalanırken beklenmeyen bir hata oluştu: {error}"
    ),
    "Approximate context window usage for {model}, in tokens:": (
        "{model} için yaklaşık bağlam penceresi kullanımı (token "
        "cinsinden):"
    ),
    (
        "Ask for changes to your code (using the best edit format)."
    ): (
        "Kodunuzda değişiklik isteyin (en uygun düzenleme biçimini "
        "kullanarak)."
    ),
    (
        "Ask for changes to your code. If no prompt provided, switches to "
        "code mode."
    ): (
        "Kodunuzda değişiklik isteyin. İstem verilmezse code moduna "
        "geçer."
    ),
    "Ask questions about aider": "Aider hakkında sorular sorun",
    (
        "Ask questions about the code base without editing any files. If "
        "no prompt provided, switches to ask mode."
    ): (
        "Hiçbir dosyayı düzenlemeden kod tabanı hakkında sorular sorun. "
        "İstem verilmezse ask moduna geçer."
    ),
    "Ask questions about your code without making any changes.": (
        "Kodunuz hakkında, herhangi bir değişiklik yapmadan sorular "
        "sorun."
    ),
    (
        "Auto mode in a trusted folder skips file prompts and also runs "
        "shell commands without asking."
    ): (
        "Güvenilir bir klasörde otomatik mod dosya istemlerini atlar ve "
        "kabuk komutlarını da sormadan çalıştırır."
    ),
    "Auto mode is now in effect for this folder.": "Otomatik mod artık bu klasör için etkin.",
    (
        "Auto mode only takes effect in trusted folders, and this folder "
        "is not trusted. Prompts will still be shown."
    ): (
        "Otomatik mod yalnızca güvenilir klasörlerde etkili olur ve bu "
        "klasör güvenilir değil. İstemler yine gösterilecek."
    ),
    (
        "Auto mode: files in this folder are added and edited without "
        "asking, and shell commands run without asking."
    ): (
        "Otomatik mod: bu klasördeki dosyalar sormadan eklenir ve "
        "düzenlenir, kabuk komutları da sormadan çalışır."
    ),
    (
        "Auto-approved: add {k_tokens:.1f}k tokens of output of {args}"
    ): (
        "Otomatik onaylandı: {args} çıktısının {k_tokens:.1f}k token'ı "
        "eklendi"
    ),
    "Auto-summarize threshold set to {new_max:,} tokens.": (
        "Otomatik özetleme eşiği {new_max:,} token olarak ayarlandı."
    ),
    (
        "Auto-summarize threshold: {max_tokens:,} tokens (model context "
        "window: {ctx} tokens); {trigger} (set with --auto-compact-at)."
    ): (
        "Otomatik özetleme eşiği: {max_tokens:,} token (model bağlam "
        "penceresi: {ctx} token); {trigger} (--auto-compact-at ile "
        "ayarlanır)."
    ),
    (
        "Automatically identify which files will need to be edited."
    ): (
        "Düzenlenmesi gereken dosyaları otomatik olarak belirleyin."
    ),
    "Can not add {abs_file_path}, which is not within {root}": (
        "{abs_file_path} eklenemiyor, {root} dizini içinde değil"
    ),
    "Can't add {matched_file} which is in gitignore": (
        "{matched_file} gitignore içinde olduğu için eklenemiyor"
    ),
    (
        "Cannot add image file {fname} as the {model} does not support "
        "images."
    ): (
        "{fname} resim dosyası eklenemiyor, {model} resimleri "
        "desteklemiyor."
    ),
    (
        "Cannot add {matched_file} as it's not part of the repository"
    ): (
        "{matched_file} deponun bir parçası olmadığı için eklenemiyor"
    ),
    "Chat mode \"{ef}\" should be one of these:\n": (
        "Sohbet modu \"{ef}\" şunlardan biri olmalıdır:\n"
    ),
    "Chat mode should be one of these:\n": "Sohbet modu şunlardan biri olmalıdır:\n",
    "Clear the chat history": "Sohbet geçmişini temizle",
    (
        "Command '{cmd}' is only supported in interactive mode, skipping."
    ): (
        "'{cmd}' komutu yalnızca etkileşimli modda desteklenir, "
        "atlanıyor."
    ),
    (
        "Commit edits to the repo made outside the chat (commit message "
        "optional)"
    ): (
        "Sohbet dışında yapılan düzenlemeleri depoya commit edin (commit "
        "mesajı isteğe bağlı)"
    ),
    "Compacted chat history: {before} -> {after} tokens.": (
        "Sohbet geçmişi sıkıştırıldı: {before} -> {after} token."
    ),
    "Converted {rel_fname} to read-only": "{rel_fname} salt okunur yapıldı",
    "Copied code context to clipboard.": "Kod bağlamı panoya kopyalandı.",
    (
        "Copied last assistant message to clipboard. Preview: {preview}"
    ): (
        "Son asistan mesajı panoya kopyalandı. Önizleme: {preview}"
    ),
    (
        "Copy the current chat context as markdown, suitable to paste "
        "into a web UI"
    ): (
        "Geçerli sohbet bağlamını, bir web arayüzüne yapıştırmaya uygun "
        "markdown olarak kopyalayın"
    ),
    "Copy the last assistant message to the clipboard": "Son asistan mesajını panoya kopyalayın",
    "Current reasoning effort: {value}": "Geçerli akıl yürütme çabası: {value}",
    (
        "Current thinking token budget: {budget:,} tokens "
        "({formatted_budget})."
    ): (
        "Geçerli düşünme token bütçesi: {budget:,} token "
        "({formatted_budget})."
    ),
    "Diff since {commit}...": "{commit} sonrasındaki fark...",
    "Directory {fname} is not in git.": "{fname} dizini git içinde değil.",
    "Display the diff of changes since the last message": (
        "Son mesajdan bu yana yapılan değişikliklerin farkını göster"
    ),
    "Drop all files and clear the chat history": "Tüm dosyaları bırak ve sohbet geçmişini temizle",
    (
        "Dropping all files from the chat session except originally "
        "read-only files."
    ): (
        "Başlangıçta salt okunur olanlar dışında tüm dosyalar sohbet "
        "oturumundan bırakılıyor."
    ),
    "Dropping all files from the chat session.": "Tüm dosyalar sohbet oturumundan bırakılıyor.",
    "Editor model": "Editör modeli",
    (
        "Enter architect/editor mode using 2 different models. If no "
        "prompt provided, switches to architect/editor mode."
    ): (
        "İki farklı model kullanarak mimar/editör moduna girin. İstem "
        "verilmezse mimar/editör moduna geçer."
    ),
    (
        "Enter context mode to see surrounding code context. If no prompt "
        "provided, switches to context mode."
    ): (
        "Çevredeki kod bağlamını görmek için bağlam moduna girin. İstem "
        "verilmezse bağlam moduna geçer."
    ),
    "Error creating file {fname}: {error}": "{fname} dosyası oluşturulurken hata: {error}",
    "Error processing clipboard content: {error}": "Pano içeriği işlenirken hata: {error}",
    "Error reading file: {error}": "Dosya okunurken hata: {error}",
    "Error restoring {file_path}, aborting undo.": (
        "{file_path} geri yüklenirken hata oluştu, geri alma iptal "
        "ediliyor."
    ),
    "Error running /git command: {error}": "/git komutu çalıştırılırken hata: {error}",
    "Error saving commands to file: {error}": "Komutlar dosyaya kaydedilirken hata: {error}",
    "Exit the application": "Uygulamadan çık",
    "Failed to copy to clipboard: {error}": "Panoya kopyalanamadı: {error}",
    "File not found: {args}": "Dosya bulunamadı: {args}",
    (
        "Find local model servers (Ollama, LM Studio, llama.cpp) and list "
        "their models"
    ): (
        "Yerel model sunucularını (Ollama, LM Studio, llama.cpp) bulun ve "
        "modellerini listeleyin"
    ),
    "Fix lint errors in {fname}?": "{fname} içindeki lint hatalarını düzeltilsin mi?",
    "Force a refresh of the repository map": "Depo haritasını zorla yenile",
    "Get help about using aider (usage, config, troubleshoot).": (
        "Aider'ı kullanma hakkında yardım alın (kullanım, yapılandırma, "
        "sorun giderme)."
    ),
    "Install one with: ollama pull <model>": "Bir tane kurmak için: ollama pull <model>",
    (
        "Lint and fix in-chat files or all dirty files if none in chat"
    ): (
        "Sohbetteki dosyaları denetleyin ve düzeltin; sohbette dosya "
        "yoksa değiştirilmiş tüm dosyaları"
    ),
    (
        "List all known files and indicate which are included in the chat "
        "session"
    ): (
        "Bilinen tüm dosyaları listeleyin ve hangilerinin sohbet "
        "oturumuna dahil olduğunu belirtin"
    ),
    (
        "List models available on a local Ollama server: /ollama "
        "[base_url]"
    ): (
        "Yerel bir Ollama sunucusundaki kullanılabilir modelleri "
        "listeleyin: /ollama [base_url]"
    ),
    "Load and execute commands from a file": "Bir dosyadaki komutları yükleyin ve çalıştırın",
    "Main model": "Ana model",
    (
        "Moved {matched_file} from read-only to editable files in the "
        "chat"
    ): (
        "{matched_file} sohbette salt okunurdan düzenlenebilir dosyalara "
        "taşındı"
    ),
    (
        "Moved {original_name} from editable to read-only files in the "
        "chat"
    ): (
        "{original_name} sohbette düzenlenebilir dosyalardan salt okunur "
        "dosyalara taşındı"
    ),
    "No assistant messages found to copy.": "Kopyalanacak asistan mesajı bulunamadı.",
    "No changes to display since the last message.": (
        "Son mesajdan bu yana gösterilecek değişiklik yok."
    ),
    "No description": "Açıklama yok",
    "No description available.": "Açıklama yok.",
    "No dirty files to lint.": "Denetlenecek değiştirilmiş dosya yok.",
    "No files matched '{word}'. Do you want to create {fname}?": (
        "'{word}' ile eşleşen dosya yok. {fname} oluşturulsun mu?"
    ),
    "No git repository found.": "Git deposu bulunamadı.",
    "No image or text content found in clipboard.": "Panoda resim veya metin içeriği bulunamadı.",
    "No local model servers found. Checked:": "Yerel model sunucusu bulunamadı. Denenen adresler:",
    "No longer trusted: {root}": "Artık güvenilmiyor: {root}",
    (
        "No match, and cannot create file with wildcard characters: "
        "{fname}"
    ): (
        "Eşleşme yok ve joker karakter içeren dosya oluşturulamaz: "
        "{fname}"
    ),
    "No matches found for: {pattern}": "Eşleşme bulunamadı: {pattern}",
    "No models are installed on the Ollama server.": "Ollama sunucusunda kurulu model yok.",
    "No more changes to commit.": "Commit edilecek başka değişiklik yok.",
    "No new files added from directory {original_name}.": (
        "{original_name} dizininden yeni dosya eklenmedi."
    ),
    "No repository map available.": "Kullanılabilir depo haritası yok.",
    "Not a file or directory: {abs_path}": "Dosya veya dizin değil: {abs_path}",
    "Nothing to compact.": "Sıkıştırılacak bir şey yok.",
    "Now at:  {commit_hash} {commit_message}": "Şimdi:  {commit_hash} {commit_message}",
    "Open an editor to write a prompt": "Bir istem yazmak için düzenleyici açın",
    (
        "Paste image/text from the clipboard into the chat.        "
        "Optionally provide a name for the image."
    ): (
        "Panodaki resmi veya metni sohbete yapıştırın. İsteğe bağlı "
        "olarak resim için bir ad verebilirsiniz."
    ),
    "Permission mode set to {value}": "İzin modu {value} olarak ayarlandı",
    "Permission mode: ask": "İzin modu: ask",
    "Permission mode: {mode}": "İzin modu: {mode}",
    (
        "Plan a multi-step change, then carry out each step with the "
        "editor model. Usage: /plan <request>"
    ): (
        "Çok adımlı bir değişikliği planlayın, ardından her adımı editör "
        "modeliyle uygulayın. Kullanım: /plan <request>"
    ),
    "Please provide a URL to scrape.": "Kazınacak bir URL girin.",
    "Please provide a filename containing commands to load.": (
        "Yüklenecek komutları içeren bir dosya adı girin."
    ),
    "Please provide a filename to save the commands to.": (
        "Komutların kaydedileceği bir dosya adı girin."
    ),
    "Please provide a partial model name to search for.": "Aramak için kısmi bir model adı girin.",
    "Print out the current repository map": "Geçerli depo haritasını yazdır",
    "Print out the current settings": "Geçerli ayarları yazdır",
    "Reasoning effort is not currently set.": "Akıl yürütme çabası şu anda ayarlı değil.",
    (
        "Remove files from the chat session to free up context space"
    ): (
        "Bağlamda yer açmak için dosyaları sohbet oturumundan kaldırın"
    ),
    "Removed read-only file {matched_file} from the chat": (
        "Salt okunur {matched_file} dosyası sohbetten kaldırıldı"
    ),
    (
        "Removed trust for {root}, but it is still trusted through "
        "{parent}. Run /permissions untrust from that folder to remove "
        "it."
    ): (
        "{root} için güven kaldırıldı, ancak hâlâ {parent} üzerinden "
        "güveniliyor. Kaldırmak için o klasörden /permissions untrust "
        "çalıştırın."
    ),
    "Removed {matched_file} from the chat": "{matched_file} sohbetten kaldırıldı",
    "Removed: {commit_hash} {commit_message}": "Kaldırıldı: {commit_hash} {commit_message}",
    "Replaced existing image in the chat: {existing_file}": (
        "Sohbetteki mevcut resim değiştirildi: {existing_file}"
    ),
    "Repo files not in the chat:\n": "Sohbette olmayan depo dosyaları:\n",
    "Report a problem by opening a GitHub Issue": "Bir GitHub Issue açarak sorunu bildirin",
    (
        "Report on the number of tokens used by the current chat context"
    ): (
        "Geçerli sohbet bağlamının kullandığı token sayısını raporlayın"
    ),
    "Restored files:": "Geri yüklenen dosyalar:",
    "Root: {root}": "Kök: {root}",
    "Run a git command (output excluded from chat)": (
        "Bir git komutu çalıştırın (çıktı sohbete dahil edilmez)"
    ),
    (
        "Run a shell command and add the output to the chat on non-zero "
        "exit code"
    ): (
        "Bir kabuk komutu çalıştırın ve sıfır olmayan çıkış kodunda "
        "çıktıyı sohbete ekleyin"
    ),
    (
        "Run a shell command and optionally add the output to the chat "
        "(alias: !)"
    ): (
        "Bir kabuk komutu çalıştırın ve isteğe bağlı olarak çıktısını "
        "sohbete ekleyin (takma ad: !)"
    ),
    (
        "Save commands to a file that can reconstruct the current chat "
        "session's files"
    ): (
        "Geçerli sohbet oturumunun dosyalarını yeniden oluşturabilecek "
        "komutları bir dosyaya kaydedin"
    ),
    "Saved commands to {path}": "Komutlar şuraya kaydedildi: {path}",
    (
        "Scrape a webpage, convert to markdown and send in a message"
    ): (
        "Bir web sayfasını kazıyın, markdown'a çevirin ve bir mesajda "
        "gönderin"
    ),
    "Scraping {url}...": "{url} kazınıyor...",
    "Search the list of available models": "Kullanılabilir modeller listesinde arama yapın",
    "Set LM_STUDIO_API_BASE={base_url} for this session.": (
        "Bu oturum için LM_STUDIO_API_BASE={base_url} ayarlandı."
    ),
    (
        "Set reasoning effort (number, low/medium/high, or auto; depends "
        "on model)"
    ): (
        "Akıl yürütme çabasını ayarlayın (sayı, low/medium/high veya "
        "auto; modele bağlıdır)"
    ),
    "Set reasoning effort to {value}": "Akıl yürütme çabası {value} olarak ayarlandı",
    (
        "Set the permission mode or folder trust: /permissions "
        "[ask|auto|trust|untrust]"
    ): (
        "İzin modunu veya klasör güvenini ayarlayın: /permissions "
        "[ask|auto|trust|untrust]"
    ),
    (
        "Set the thinking token budget, eg: 8096, 8k, 10.5k, 0.5M, or 0 "
        "to disable."
    ): (
        "Düşünme token bütçesini ayarlayın, ör: 8096, 8k, 10.5k, 0.5M ya "
        "da kapatmak için 0."
    ),
    (
        "Set thinking token budget to {budget:,} tokens "
        "({formatted_budget})."
    ): (
        "Düşünme token bütçesi {budget:,} token ({formatted_budget}) "
        "olarak ayarlandı."
    ),
    (
        "Show or set when chat history is auto-summarized: /autocompact "
        "[N | N% | default]"
    ): (
        "Sohbet geçmişinin ne zaman otomatik özetleneceğini gösterin veya "
        "ayarlayın: /autocompact [N | N% | default]"
    ),
    "Skipping {fname} due to aiderignore or --subtree-only.": (
        "{fname} aiderignore veya --subtree-only nedeniyle atlanıyor."
    ),
    (
        "Start one, or point pairforge at it with OLLAMA_API_BASE, "
        "LM_STUDIO_API_BASE or LLAMA_CPP_API_BASE."
    ): (
        "Birini başlatın ya da pairforge'u OLLAMA_API_BASE, "
        "LM_STUDIO_API_BASE veya LLAMA_CPP_API_BASE ile ona yönlendirin."
    ),
    "Summarize the chat history now to free up context": (
        "Bağlamda yer açmak için sohbet geçmişini şimdi özetle"
    ),
    "Switch the Editor Model to a new LLM": "Editör modelini yeni bir LLM'e değiştirin",
    "Switch the Main Model to a new LLM": "Ana modeli yeni bir LLM'e değiştirin",
    "Switch the Weak Model to a new LLM": "Zayıf modeli yeni bir LLM'e değiştirin",
    "Switch to a new chat mode": "Yeni bir sohbet moduna geçin",
    (
        "The file {fname} has uncommitted changes. Please stash them "
        "before undoing."
    ): (
        "{fname} dosyasında commit edilmemiş değişiklikler var. Geri "
        "almadan önce lütfen bunları stash'leyin."
    ),
    (
        "The file {fname} was not in the repository in the previous "
        "commit. Cannot undo safely."
    ): (
        "{fname} dosyası önceki commit'te depoda yoktu. Güvenli bir "
        "şekilde geri alınamıyor."
    ),
    (
        "The last commit has already been pushed to the origin. Undoing "
        "is not possible."
    ): (
        "Son commit zaten origin'e gönderilmiş. Geri alma mümkün değil."
    ),
    (
        "The last commit was not made by aider in this chat session."
    ): (
        "Son commit bu sohbet oturumunda aider tarafından yapılmadı."
    ),
    (
        "The last commit {hexsha} has more than 1 parent, can't undo."
    ): (
        "Son commit {hexsha} birden fazla ebeveyne sahip, geri alınamaz."
    ),
    (
        "The model's context window size is unknown, so N% cannot be "
        "used."
    ): (
        "Modelin bağlam penceresi boyutu bilinmiyor, bu yüzden N% "
        "kullanılamaz."
    ),
    "The repo map has been refreshed, use /map to view it.": (
        "Depo haritası yenilendi, görüntülemek için /map kullanın."
    ),
    "Thinking tokens are not currently set.": "Düşünme token'ları şu anda ayarlı değil.",
    "Thinking tokens disabled.": "Düşünme token'ları devre dışı bırakıldı.",
    "This is the first commit in the repository. Cannot undo.": (
        "Bu, depodaki ilk commit. Geri alınamaz."
    ),
    (
        "To use these, start pairforge with OPENAI_API_BASE={base_url}"
    ): (
        "Bunları kullanmak için pairforge'u OPENAI_API_BASE={base_url} "
        "ile başlatın"
    ),
    (
        "Toggle multiline mode (swaps behavior of Enter and Meta+Enter)"
    ): (
        "Çok satırlı modu aç/kapat (Enter ve Meta+Enter davranışını "
        "değiştirir)"
    ),
    "Trusted folder: {root}": "Güvenilir klasör: {root}",
    "Trusted: {trusted}": "Güvenilir: {trusted}",
    "Unable to complete commit: {err}": "Commit tamamlanamadı: {err}",
    "Unable to complete undo: {err}": "Geri alma tamamlanamadı: {err}",
    (
        "Unable to get current commit. The repository might be empty."
    ): (
        "Geçerli commit alınamadı. Depo boş olabilir."
    ),
    "Unable to initialize interactive help.": "Etkileşimli yardım başlatılamadı.",
    "Unable to initialize playwright.": "Playwright başlatılamadı.",
    "Unable to lint {fname}": "{fname} denetlenemedi",
    "Unable to read {matched_file}": "{matched_file} okunamadı",
    "Unable to restore files:": "Geri yüklenemeyen dosyalar:",
    "Undo the last git commit if it was done by aider": (
        "Aider tarafından yapıldıysa son git commit'ini geri al"
    ),
    (
        "Usage: /autocompact [N | N% | default]  (N > 0, N% is 1-100)"
    ): (
        "Kullanım: /autocompact [N | N% | default]  (N > 0, N% 1-100 "
        "arasında)"
    ),
    "Usage: /permissions [ask|auto|trust|untrust]": (
        "Kullanım: /permissions [ask|auto|trust|untrust]"
    ),
    "Usage: /plan <request>": "Kullanım: /plan <request>",
    (
        "Use `/help <question>` to ask questions about how to use aider."
    ): (
        "Aider'ın kullanımı hakkında sorular sormak için `/help <soru>` "
        "kullanın."
    ),
    "Use one with: /model <name>": "Birini kullanmak için: /model <name>",
    "Use one with: /model ollama_chat/<name>": "Birini kullanmak için: /model ollama_chat/<name>",
    "Weak model": "Zayıf model",
    (
        "Work with an architect model to design code changes, and an "
        "editor to make them."
    ): (
        "Kod değişikliklerini tasarlamak için bir mimar modeliyle, "
        "bunları uygulamak için bir editör modeliyle çalışın."
    ),
    "You can add to git with: /git add {fname}": "Git'e şununla ekleyebilirsiniz: /git add {fname}",
    (
        "You could try `/git reset --hard HEAD^` but be aware that this "
        "is a destructive command!"
    ): (
        "`/git reset --hard HEAD^` komutunu deneyebilirsiniz, ancak bunun "
        "yıkıcı bir komut olduğunu unutmayın!"
    ),
    (
        "You may need to install xclip or xsel on Linux, or pbcopy on "
        "macOS."
    ): (
        "Linux'ta xclip veya xsel, macOS'ta pbcopy kurmanız gerekebilir."
    ),
    (
        "also when the whole prompt passes {percent}% of the context "
        "window"
    ): (
        "ayrıca tüm istem bağlam penceresinin %{percent}'ini aştığında"
    ),
    "chat history": "sohbet geçmişi",
    "line": "satır",
    "lines": "satır",
    "repository map": "depo haritası",
    "system messages": "sistem mesajları",
    "unknown": "bilinmiyor",
    "use --map-tokens to resize": "boyutlandırmak için --map-tokens kullanın",
    "use /clear to clear": "temizlemek için /clear kullanın",
    "whole-prompt trigger is off": "tüm istem tetikleyicisi kapalı",
    "{cost_pad}{limit} tokens max context window size": (
        "{cost_pad}{limit} token en büyük bağlam penceresi boyutu"
    ),
    "{cost_pad}{remaining} tokens remaining in context window": (
        "{cost_pad}{remaining} token bağlam penceresinde kaldı"
    ),
    (
        "{cost_pad}{remaining} tokens remaining in context window (use "
        "/drop or /clear to make space)"
    ): (
        "{cost_pad}{remaining} token bağlam penceresinde kaldı (yer açmak "
        "için /drop veya /clear kullanın)"
    ),
    (
        "{cost_pad}{remaining} tokens remaining, window exhausted (use "
        "/drop or /clear to make space)"
    ): (
        "{cost_pad}{remaining} token kaldı, bağlam penceresi doldu (yer "
        "açmak için /drop veya /clear kullanın)"
    ),
    "{fname} (read-only)": "{fname} (salt okunur)",
    "{label} ({name}):": "{label} ({name}):",
    "{matched_file} is already in the chat as an editable file": (
        "{matched_file} zaten sohbette düzenlenebilir dosya olarak var"
    ),
    "{name} at {base_url}:": "{name}, {base_url} adresinde:",
    (
        "{original_name} is already in the chat as a read-only file"
    ): (
        "{original_name} zaten sohbette salt okunur dosya olarak var"
    ),
}
