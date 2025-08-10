use mensa_api::cache::Cache;
use serde_json;
use std::ffi::CString;
use std::os::raw::c_char;

#[unsafe(no_mangle)]
pub extern "C" fn compute() -> *mut c_char {
    let rt = tokio::runtime::Builder::new_current_thread()
    .enable_all()
    .build()
    .unwrap();
    let result = rt.block_on(fetch_menu());
    match result {
        Ok(s) => s.into_raw(),
        Err(_) => CString::new("").unwrap().into_raw(),
    }
}

async fn fetch_menu() -> Result<CString, Box<dyn std::error::Error>> {
    // Fetch the data
    let menu_data = Cache::fetch_data().await;
    let menu = menu_data.unwrap();
    let meals = menu.get_meals();

    // Convert to JSON
    let json_str = serde_json::to_string_pretty(&meals)?;

    Ok(CString::new(json_str)?)
}

#[unsafe(no_mangle)]
pub extern "C" fn free_string(s: *mut c_char) {
    if s.is_null() { return; }
    unsafe { let _ = CString::from_raw(s); }
}

