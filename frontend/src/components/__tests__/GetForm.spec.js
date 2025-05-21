import { mount } from '@vue/test-utils'
import GetForm from '../GetForm.vue'

describe('GetForm.vue', () => {
  it('emits submit with key', async () => {
    const wrapper = mount(GetForm)
    await wrapper.find('input').setValue('abc')
    await wrapper.find('button').trigger('submit')
    expect(wrapper.emitted('submit')[0][0]).toBe('abc')
  })
})