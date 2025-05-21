import { mount } from '@vue/test-utils'
import DeleteForm from '../DeleteForm.vue'

describe('DeleteForm.vue', () => {
  it('emits submit with key', async () => {
    const wrapper = mount(DeleteForm)
    await wrapper.find('input').setValue('xyz')
    await wrapper.find('button').trigger('submit')
    expect(wrapper.emitted('submit')[0][0]).toBe('xyz')
  })
})