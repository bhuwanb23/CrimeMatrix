import { get, post, put, del } from './api'

export async function listBookmarks(entityType = null, userId = 1) {
  const params = new URLSearchParams({ user_id: userId })
  if (entityType) params.append('entity_type', entityType)
  return get(`/bookmarks/?${params.toString()}`)
}

export async function getGroupedBookmarks(userId = 1) {
  return get(`/bookmarks/grouped?user_id=${userId}`)
}

export async function checkBookmark(entityType, entityId, userId = 1) {
  return get(`/bookmarks/check?user_id=${userId}&entity_type=${entityType}&entity_id=${entityId}`)
}

export async function getBookmarkCount(entityType, entityId) {
  return get(`/bookmarks/count?entity_type=${entityType}&entity_id=${entityId}`)
}

export async function createBookmark(entityType, entityId, note = null, userId = 1) {
  return post('/bookmarks/', {
    user_id: userId,
    entity_type: entityType,
    entity_id: entityId,
    bookmark_note: note,
  })
}

export async function toggleBookmark(entityType, entityId, note = null, userId = 1) {
  return post('/bookmarks/toggle', {
    user_id: userId,
    entity_type: entityType,
    entity_id: entityId,
    bookmark_note: note,
  })
}

export async function updateBookmarkNote(bookmarkId, note) {
  return put(`/bookmarks/${bookmarkId}/note`, { bookmark_note: note })
}

export async function removeBookmark(bookmarkId) {
  return del(`/bookmarks/${bookmarkId}`)
}

export async function removeBookmarkByEntity(entityType, entityId, userId = 1) {
  return del(`/bookmarks/?user_id=${userId}&entity_type=${entityType}&entity_id=${entityId}`)
}
