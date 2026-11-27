"""Turkish messages for aider/coders/*."""

MESSAGES = {
    "\n\n^C again to exit": "\n\nÇıkmak için ^C tuşuna tekrar basın",
    " -- possibly exceeded output limit!": " -- çıktı sınırı aşılmış olabilir!",
    " -- possibly exhausted context window!": " -- bağlam penceresi tükenmiş olabilir!",
    ", infinite output": ", sınırsız çıktı",
    ", prompt cache": ", istem önbelleği",
    ", reasoning {effort}": ", akıl yürütme {effort}",
    ", {tokens} cache hit": ", {tokens} önbellek isabeti",
    ", {tokens} cache write": ", {tokens} önbelleğe yazıldı",
    ", {tokens} received.": ", {tokens} alındı.",
    ", {tokens} think tokens": ", {tokens} düşünme belirteci",
    "- Ask for smaller changes in each request.": "- Her istekte daha küçük değişiklikler isteyin.",
    "- Break your code into smaller files": "- Kodunuzu daha küçük dosyalara bölün",
    "- Break your code into smaller source files.": "- Kaynak kodunuzu daha küçük dosyalara bölün.",
    "- Use /clear to clear the chat history": "- Sohbet geçmişini temizlemek için /clear kullanın",
    "- Use /clear to clear the chat history.": (  # noqa: E501
        "- Sohbet geçmişini temizlemek için /clear kullanın."
    ),
    "- Use /drop to remove unneeded files from the chat": (
        "- Gereksiz dosyaları sohbetten çıkarmak için /drop kullanın"
    ),
    "- Use /drop to remove unneeded files from the chat session.": (
        "- Gereksiz dosyaları sohbet oturumundan çıkarmak için /drop kullanın."
    ),
    "- Use /tokens to see token usage.": "- Belirteç kullanımını görmek için /tokens kullanın.",
    "- Use a stronger model that can return diffs.": (
        "- Diff döndürebilen daha güçlü bir model kullanın."
    ),
    "Add URL to the chat?": "URL sohbete eklensin mi?",
    "Add command output to the chat?": "Komut çıktısı sohbete eklensin mi?",
    "Add file to the chat?": "Dosya sohbete eklensin mi?",
    "Added {count} {line_plural} of output to the chat.": (
        "Sohbete {count} {line_plural} çıktı eklendi."
    ),
    "Added {fname} to the chat (read-only).": "{fname} sohbete eklendi (salt okunur).",
    "Added {fname} to the chat.": "{fname} sohbete eklendi.",
    "Adding {path}": "{path} ekleniyor",
    "Allow edits to file that has not been added to the chat?": (
        "Sohbete eklenmemiş dosyada değişikliklere izin verilsin mi?"
    ),
    "Applied edit to {path}": "{path} dosyasındaki düzenleme uygulandı",
    "Attempt to fix lint errors?": "Lint hataları düzeltilmeye çalışılsın mı?",
    "Attempt to fix test errors?": "Test hataları düzeltilmeye çalışılsın mı?",
    "Auto effort: {effort}": "Otomatik çaba: {effort}",
    "Auto-added {fname} (permission mode: auto)": "{fname} otomatik eklendi (izin modu: auto)",
    "Auto-approved: {description}": "Otomatik onaylandı: {description}",
    "Cache warming error: {err}": "Önbellek ısındırma hatası: {err}",
    "Can not create {fname}, skipping.": "{fname} oluşturulamadı, atlanıyor.",
    "Chat history summarization failed, continuing with full history": (
        "Sohbet geçmişi özetlenemedi, tam geçmişle devam ediliyor"
    ),
    "Chat history summarized: {history_tokens:,} -> {new_tokens:,} tokens.": (
        "Sohbet geçmişi özetlendi: {history_tokens:,} -> {new_tokens:,} belirteç."
    ),
    "Committing {path} before applying edits.": (
        "Düzenlemeler uygulanmadan önce {path} commit ediliyor."
    ),
    "Context is {percent}% full ({total:,} of {window:,} tokens); summarizing the chat history...": (  # noqa: E501
        "Bağlam %{percent} dolu ({total:,} / {window:,} belirteç); sohbet geçmişi özetleniyor..."
    ),
    "Cost: ${message_cost} message, ${total_cost} session.": (
        "Maliyet: ${message_cost} bu mesaj, ${total_cost} oturum."
    ),
    "Could not summarize the chat history: {err}": "Sohbet geçmişi özetlenemedi: {err}",
    "Create new file?": "Yeni dosya oluşturulsun mu?",
    "Creating empty file {fname}": "Boş {fname} dosyası oluşturuluyor",
    "DELETE Warning: File not found, skipping: {path}": (
        "DELETE uyarısı: Dosya bulunamadı, atlanıyor: {path}"
    ),
    "Deleting {path}": "{path} siliniyor",
    "Did not apply edit to {path} (--dry-run)": (
        "{path} dosyasına düzenleme uygulanmadı (--dry-run)"
    ),
    "Dropping {fname} from the chat.": "{fname} sohbetten çıkarılıyor.",
    "Duplicate delete action for file: {path} ignored.": (
        "Dosya için yinelenen silme işlemi yok sayıldı: {path}"
    ),
    "Edit the files?": "Dosyalar düzenlensin mi?",
    "Editor model: {model} with {edit_format} edit format": (
        "Düzenleyici model: {model}, {edit_format} düzenleme biçimiyle"
    ),
    "Empty response received from LLM. Check your provider account?": (
        "LLM'den boş yanıt alındı. Sağlayıcı hesabınızı kontrol edin?"
    ),
    "Error: Read-only file {fname} does not exist. Skipping.": (
        "Hata: Salt okunur {fname} dosyası yok. Atlanıyor."
    ),
    "Exception while updating files:": "Dosyalar güncellenirken istisna oluştu:",
    "Failed to apply edit to {path}": "{path} dosyasına düzenleme uygulanamadı",
    "Finished summarizing chat history.": "Sohbet geçmişi özetlemesi tamamlandı.",
    "Git repo: none": "Git deposu: yok",
    "Git repo: {repo_dir} with {num_files:,} files": (
        "Git deposu: {repo_dir}, {num_files:,} dosya ile"
    ),
    "Input tokens: ~{input_tokens:,} of {max_input_tokens:,}{inp_err}": (
        "Giriş belirteçleri: ~{input_tokens:,} / {max_input_tokens:,}{inp_err}"
    ),
    "It's probably safe to try and send the request, most providers won't charge if the context limit is exceeded.": (  # noqa: E501
        "İsteği göndermek muhtemelen güvenlidir; çoğu sağlayıcı bağlam sınırı aşılırsa ücret almaz."
    ),
    "JSON Schema:": "JSON Şeması:",
    "Main model: {model} with {edit_format} edit format": (
        "Ana model: {model}, {edit_format} düzenleme biçimiyle"
    ),
    "Model {model} has hit a token limit!": "{model} modeli belirteç sınırına ulaştı!",
    "Model: {model} with {edit_format} edit format": (
        "Model: {model}, {edit_format} düzenleme biçimiyle"
    ),
    "Multiline mode: Enabled. Enter inserts newline, Alt-Enter submits text": (
        "Çok satırlı mod: Açık. Enter yeni satır ekler, Alt-Enter metni gönderir"
    ),
    "Only {count} reflections allowed, stopping.": (
        "Yalnızca {count} yansıtmaya izin veriliyor, duruluyor."
    ),
    "Output tokens: ~{output_tokens:,} of {max_output_tokens:,}{out_err}": (
        "Çıktı belirteçleri: ~{output_tokens:,} / {max_output_tokens:,}{out_err}"
    ),
    "Patch format warning: Missing '*** Begin Patch'/'*** End Patch' sentinels.": (
        "Yama biçimi uyarısı: '*** Begin Patch' / '*** End Patch' işaretleri eksik."
    ),
    "Plan ({total} steps):": "Plan ({total} adım):",
    "Plan complete: {total} steps done.": "Plan tamamlandı: {total} adım bitti.",
    "Plan not run.": "Plan çalıştırılmadı.",
    "Plan stopped by user after {done} of {total} steps.": (
        "Plan kullanıcı tarafından durduruldu: {total} adımdan {done} tanesinden sonra."
    ),
    "Repo-map: disabled": "Repo-map: devre dışı",
    "Repo-map: disabled because map_tokens == 0": (
        "Repo-map: map_tokens == 0 olduğu için devre dışı"
    ),
    "Repo-map: using {map_tokens} tokens, {refresh} refresh": (
        "Repo-map: {map_tokens} belirteç kullanıyor, {refresh} yenileme"
    ),
    "Response does not appear to be in patch format.": "Yanıt yama biçiminde görünmüyor.",
    "Restored previous conversation history.": "Önceki sohbet geçmişi geri yüklendi.",
    "Retrying in {delay:.1f} seconds...": "{delay:.1f} saniye içinde yeniden denenecek...",
    "Run shell command?": "Kabuk komutu çalıştırılsın mı?",
    "Run shell commands?": "Kabuk komutları çalıştırılsın mı?",
    "Run this plan?": "Bu plan çalıştırılsın mı?",
    "Running {command}": "{command} çalıştırılıyor",
    "See: {url}": "Bkz: {url}",
    "Skipping edits to {path}": "{path} için düzenlemeler atlanıyor",
    "Skipping edits to {path} that matches gitignore spec.": (
        "{path} için düzenlemeler atlanıyor (gitignore kuralına uyuyor)."
    ),
    "Skipping {fname} that is not a normal file.": (
        "{fname} normal bir dosya olmadığı için atlanıyor."
    ),
    "Skipping {fname} that matches aiderignore spec.": (
        "{fname} aiderignore kuralına uyduğu için atlanıyor."
    ),
    "Skipping {fname} that matches gitignore spec.": (
        "{fname} gitignore kuralına uyduğu için atlanıyor."
    ),
    "Starting to summarize chat history.": "Sohbet geçmişi özetlenmeye başlanıyor.",
    "Step {current}/{total} failed: {err}. Plan stopped.": (
        "Adım {current}/{total} başarısız: {err}. Plan durduruldu."
    ),
    "Step {i}/{total}: {step}": "Adım {i}/{total}: {step}",
    "The LLM did not conform to the edit format.": "LLM düzenleme biçimine uymadı.",
    "The model produced malformed edits twice; switching to the whole edit format for this session.": (  # noqa: E501  # noqa: E501
        "Model iki kez hatalı düzenleme üretti; bu oturum için tüm dosya düzenleme biçimine"
        " geçiliyor."
    ),
    "The planner returned no numbered steps; nothing was run.": (
        "Planlayıcı numaralı adım döndürmedi; hiçbir şey çalıştırılmadı."
    ),
    "The summary ({new_tokens:,} tokens) was not smaller than the chat history ({history_tokens:,} tokens); keeping the history as it is.": (  # noqa: E501
        "Özet ({new_tokens:,} belirteç) sohbet geçmişinden ({history_tokens:,} belirteç) "
        "küçük değil; geçmiş olduğu gibi tutuluyor."
    ),
    "To reduce input tokens:": "Giriş belirteçlerini azaltmak için:",
    "To reduce output tokens:": "Çıktı belirteçlerini azaltmak için:",
    "To reduce the chat context:": "Sohbet bağlamını azaltmak için:",
    "Token counts below are approximate.": "Aşağıdaki belirteç sayıları yaklaşıktır.",
    "Tokens: {sent} sent": "Belirteç: {sent} gönderildi",
    "Total tokens: ~{total_tokens:,} of {max_input_tokens:,}{tot_err}": (
        "Toplam belirteç: ~{total_tokens:,} / {max_input_tokens:,}{tot_err}"
    ),
    "Try to proceed anyway?": "Yine de devam edilsin mi?",
    "UPDATE Warning: Target file for move already exists, overwriting: {move_path}": (
        "UPDATE uyarısı: Taşıma hedef dosyası zaten var, üzerine yazılıyor: {move_path}"
    ),
    "Unable to commit: {err}": "Commit yapılamadı: {err}",
    "Unable to create {path}, skipping edits.": "{path} oluşturulamadı, düzenlemeler atlanıyor.",
    "Unable to find a fencing strategy! Falling back to: {open}...{close}": (
        "Çit stratejisi bulunamadı! Şuna dönülüyor: {open}...{close}"
    ),
    "Updating and moving {path} to {move_path}": (
        "{path} güncelleniyor ve {move_path} konumuna taşınıyor"
    ),
    "Updating {path}": "{path} güncelleniyor",
    "Warmed {tokens} cached tokens.": "{tokens} önbellekli belirteç ısındırıldı.",
    "Warning: For large repos, consider using --subtree-only and .aiderignore": (
        "Uyarı: Büyük depolar için --subtree-only ve .aiderignore kullanmayı düşünün"
    ),
    "Warning: it's best to only add files that need changes to the chat.": (
        "Uyarı: Sohbete yalnızca değişiklik gereken dosyaları eklemek en iyisidir."
    ),
    "Warning: map-tokens > {max_map_tokens} is not recommended. Too much irrelevant code can confuse LLMs.": (  # noqa: E501
        "Uyarı: map-tokens > {max_map_tokens} önerilmez. "
        "Çok fazla alakasız kod LLM'leri karıştırabilir."
    ),
    "Weak model: {model}": "Hafif model: {model}",
    "You can use /undo to undo and discard each aider commit.": (
        "Her aider commit'ini geri almak ve atmak için /undo kullanabilirsiniz."
    ),
    "Your estimated chat context of {input_tokens:,} tokens exceeds the {max_input_tokens:,} token limit for {model}!": (  # noqa: E501
        "Tahmini sohbet bağlamınız {input_tokens:,} belirteç; {model} için "
        "{max_input_tokens:,} belirteç sınırını aşıyor!"
    ),
    "[ ] {i}. {step}": "[ ] {i}. {step}",
    "[x] {i}. {step}": "[x] {i}. {step}",
    "add URL {url} to the chat": "{url} adresini sohbete ekle",
    "add command output to the chat": "komut çıktısını sohbete ekle",
    "attempt to fix lint errors": "lint hatalarını düzeltmeyi dene",
    "attempt to fix test errors": "test hatalarını düzeltmeyi dene",
    "edit the files": "dosyaları düzenle",
    "effort auto": "çaba auto",
    "effort auto:{effort}": "çaba auto:{effort}",
    "effort {effort}": "çaba {effort}",
    "line": "satır",
    "lines": "satır",
    "run the {total}-step plan": "{total} adımlık planı çalıştır",
    "send the request anyway": "yine de isteği gönder",
    "{fname} is too large to add in full ({tokens:,} tokens); sent an outline instead. Use /add to edit it.": (  # noqa: E501
        "{fname} tamamen eklemek için çok büyük ({tokens:,} belirteç); "
        "bunun yerine ana hatları gönderildi. Düzenlemek için /add kullanın."
    ),
}
